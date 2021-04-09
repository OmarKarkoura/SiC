from ovito.io import import_file, export_file
from ovito.modifiers import (InvertSelectionModifier, DeleteSelectedModifier,
                             ClusterAnalysisModifier, WignerSeitzAnalysisModifier)
from ovito.pipeline import ReferenceConfigurationModifier
from ovito.data import DataTable
import numpy as np
import pandas as pd

import multiprocessing as mp
import argparse, glob, os, re, sys, time

CLUSTER_CUTOFF = 2.5 # Cluster cutoff in Angstrom
NUM_ATOM_TYPES = {"6H": 12, "4H": 8, "3C": 8}

def total_occupancy_modifier(frame, data):
    """This modifier calculates the total and elementwise site occupancy and saves
    them in new particle properties `Total Occupancy`, `Si Occupancy` and `C
    Occupancy`. It also creates properties `Is Si Site` and `Is C Site`, which
    indicate the type of site.

    """

    occupancies = data.particles['Occupancy'][...]
    site_type = data.particles['Particle Type'][...]
    num_site_types = occupancies.shape[1] #Accessing the number of columns in the Occupancy matrix
    total_occupancy = np.sum(occupancies, axis=1) #Summing over all columns
    # NOTE By convention, the first half of types is Si, the second half is C
    is_si_site = site_type <= num_site_types//2
    is_c_site = site_type > num_site_types//2
    si_occupancy = np.sum(occupancies[:, :(num_site_types//2)], axis=1)
    c_occupancy = np.sum(occupancies[:, (num_site_types//2):], axis=1)
    data.particles_.create_property('Total Occupancy', data=total_occupancy.astype(int))
    data.particles_.create_property('Is Si Site', data=is_si_site.astype(int))
    data.particles_.create_property('Is C Site', data=is_c_site.astype(int))
    data.particles_.create_property('Si Occupancy', data=si_occupancy.astype(int))
    data.particles_.create_property('C Occupancy', data=c_occupancy.astype(int))


def select_defects_modifier(frame, data):
    """This modifier selects all sites containing at least one kind of basic
    defect.

    """

    # Retrieve some relevant site properties as numpy arrays.
    occupancies = data.particles['Occupancy'][...]
    site_type = data.particles['Particle Type'][...]
    num_site_types = occupancies.shape[1]
    is_si_site = data.particles['Is Si Site'][...]
    is_c_site = data.particles['Is C Site'][...]
    si_occupancy = data.particles['Si Occupancy'][...]
    c_occupancy = data.particles['C Occupancy'][...]
    total_occupancy = data.particles['Total Occupancy'][...]

    # Set up a particle selection by creating the Selection property:
    selection = data.particles_.create_property('Selection')

    # TODO Create a mask (boolean numpy array) to identify basic defect sites
    v =data.particles["Occupancy"][np.arange(data.particles.count),(data.particles['Particle Type'][...] -1)]
    vacancy_mask =(total_occupancy ==0).astype(int)
    interstitial_mask = (total_occupancy >1).astype(int)
    antisite_mask = ((v==0) & (total_occupancy >0)).astype(int)

    data.particles_.create_property('vacancy_mask', data=vacancy_mask)
    data.particles_.create_property('interstitial_mask', data=interstitial_mask)
    data.particles_.create_property('antisite_mask', data=antisite_mask)

    selection[...] = vacancy_mask | interstitial_mask | antisite_mask
def classify_defect_clusters_modifier(frame, data):
    """This modifier identifies basic defects at each atomic site and saves the
    counts in new particle properties `Si_V` (Si vacancy), `Si_I` (Si
    interstitial), `Si_C` (Si on a C site), `C_V` (C vacancy), `C_I` (C
    interstitial) and `C_Si` (C on a Si site).

    """

    if data.particles.count == 0:
        # No particles there to classify, create empty properties anyway
        data.particles_.create_property('Si_V', dtype=int, components=1)
        data.particles_.create_property('Si_I', dtype=int, components=1)
        data.particles_.create_property('Si_C', dtype=int, components=1)
        data.particles_.create_property('C_V', dtype=int, components=1)
        data.particles_.create_property('C_I', dtype=int, components=1)
        data.particles_.create_property('C_Si', dtype=int, components=1)
        return

    # TODO Create numpy arrays containing the number of Si vacancies,
    #      interstitials, etc for each particle site in `data.particles`. These
    #      next lines are just placeholders!
    si_vacancy = data.particles["vacancy_mask"][...] * data.particles["Is Si Site"][...]
    si_interstitial = (data.particles["Is Si Site"][...] & (data.particles["Si Occupancy"][...] > 1)) * (
                data.particles["Si Occupancy"][...] - 1) + (
                                  (data.particles["Is C Site"][...]) * data.particles["Si Occupancy"][...]) - (
                                  data.particles["Is C Site"][...] & data.particles["antisite_mask"][...])
    si_antisite = data.particles["antisite_mask"][...] * data.particles["Is Si Site"][...]
    c_vacancy = data.particles["vacancy_mask"][...] * data.particles["Is C Site"][...]
    c_interstitial = (data.particles["Is C Site"][...] & (data.particles["C Occupancy"][...] > 1)) * (
                data.particles["C Occupancy"][...] - 1) + (
                                 (data.particles["Is Si Site"][...]) * data.particles["C Occupancy"][...]) - (
                                 data.particles["Is Si Site"][...] & data.particles["antisite_mask"][...])
    c_antisite = data.particles["antisite_mask"][...] * data.particles["Is C Site"][...]


    data.particles_.create_property('Si_V', data=si_vacancy.astype(int))
    data.particles_.create_property('Si_I', data=si_interstitial.astype(int))
    data.particles_.create_property('Si_C', data=si_antisite.astype(int))
    data.particles_.create_property('C_V', data=c_vacancy.astype(int))
    data.particles_.create_property('C_I', data=c_interstitial.astype(int))
    data.particles_.create_property('C_Si', data=c_antisite.astype(int))


def create_pipeline(path):
    """Create an ovito pipeline for the dump file at `path`."""

    pipeline = import_file(path)
    # Perform Wigner-Seitz analysis:
    ws = WignerSeitzAnalysisModifier(
        output_displaced=False,    # Output sites
        per_type_occupancies=True, # Output occupancies per atom type
        affine_mapping=ReferenceConfigurationModifier.AffineMapping.ToReference)
    pipeline.modifiers.append(ws)
    # Calculate total and elementwise occupancies
    pipeline.modifiers.append(total_occupancy_modifier)
    # Select all defect sites
    pipeline.modifiers.append(select_defects_modifier)
    # Delete all non-defect sites
    pipeline.modifiers.append(InvertSelectionModifier())
    pipeline.modifiers.append(DeleteSelectedModifier())
    # Find defect clusters
    pipeline.modifiers.append(ClusterAnalysisModifier(
        cutoff=CLUSTER_CUTOFF,
        sort_by_size=False))
    # Classify defect clusters
    pipeline.modifiers.append(classify_defect_clusters_modifier)

    return pipeline

def classify_clusters(data):
    if data.particles.count == 0:
        # No particles there to classify
        return None

    columns = {
        "Cluster": data.particles["Cluster"][...],
        "Si_V": data.particles["Si_V"][...],
        "Si_I": data.particles["Si_I"][...],
        "Si_C": data.particles["Si_C"][...],
        "C_V": data.particles["C_V"][...],
        "C_I": data.particles["C_I"][...],
        "C_Si": data.particles["C_Si"][...]
    }
    df = pd.DataFrame(columns).groupby("Cluster", as_index=False).aggregate(np.sum)

    # Count all unique cluster compositions
    cls = df.groupby(["Si_V", "Si_I", "Si_C", "C_V", "C_I", "C_Si"], as_index=False).size()
    return cls.rename(columns={"size": "Counts"})

def process_dumpfile(path, out_path, system):
    """Process the dump file at `path`. The processed dump file is saved in the
    directory `out_path`. The `system` argument is one of "3C", "4H" or "6H".
    The function returns a pandas DataFrame containing the number of defect
    clusters found in the last frame of the dumpfile.

    """

    pipeline = create_pipeline(path)

    # Extract energy and direction from file name

    # NOTE By convention, the dump file names follow a specific format and
    #      contain the PKA energy, initial direction, the grid ID and PKA ID.
    m = re.match(r"collision_([-0-9.]+)eV_phi([-0-9.]+)_theta([-0-9.]+)_grid([0-9]+)_PKA([0-9]+)\.dump", os.path.basename(path))
    PKA_energy = float(m.group(1))
    PKA_phi = float(m.group(2))
    PKA_theta = float(m.group(3))
    grid = int(m.group(4))
    PKA_id = int(m.group(5))
    PKA = "Si" if PKA_id <= NUM_ATOM_TYPES[system]//2 else "C"

    # Classify clusters in last frame
    clusters = classify_clusters(pipeline.compute(pipeline.source.num_frames-1))

    # Save processed dump file
    output_path = os.path.join(out_path, "processed_"+os.path.basename(path))
    columns = ["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "Cluster"]
    for i in range(12):
        columns.append("Occupancy.%d" % (i+1))
    columns += ["Total Occupancy", "Si_V", "Si_I", "Si_C", "C_V", "C_I", "C_Si"]
    export_file(pipeline, output_path, "lammps/dump", multiple_frames=True, columns=columns)

    if clusters is not None:
        clusters["PKA Energy"] = PKA_energy
        clusters["PKA Theta"] = PKA_theta
        clusters["PKA Phi"] = PKA_phi
        clusters["PKA Type"] = PKA
        clusters["PKA ID"] = PKA_id
        clusters["Grid"] = grid

    return clusters

def main(args):

    start_time = time.time()

    columns = ["PKA Type", "PKA ID", "Grid", "PKA Energy", "PKA Theta", "PKA Phi", "Si_V", "Si_I", "Si_C", "C_V", "C_I", "C_Si", "Counts"]
    all_clusters = pd.DataFrame(columns=columns)
    dump_files = glob.glob(args.file)

    print("Analyzing", args.system, "SiC collision dumps.")
    print("Processing", len(dump_files), "dump files.")
    print("Using", args.jobs, "processors.")

    try:
        if args.jobs > 1:
            with mp.Pool(processes=args.jobs) as pool:
                for (i, clusters) in enumerate(pool.imap(lambda f: process_dumpfile(f, args.output, args.system), dump_files)):
                    if clusters is not None:
                        all_clusters = all_clusters.append(clusters[columns], ignore_index=True)
                    dt = time.time()-start_time
                    print("[%d/%d] %02d:%02d:%02d" % (i+1, len(dump_files), dt//3600, (dt%3600)//60, dt%60))
        else:
            for (i, path) in enumerate(dump_files):
                clusters = process_dumpfile(path, args.output, args.system)
                if clusters is not None:
                    all_clusters = all_clusters.append(clusters[columns], ignore_index=True)

                dt = time.time()-start_time
                print("[%d/%d] %02d:%02d:%02d" % (i+1, len(dump_files), dt//3600, (dt%3600)//60, dt%60))

    finally:
        # Output cluster counts
        all_clusters.to_csv("clusters.csv", sep=",", index=False)


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze SiC collision cascades.')
    parser.add_argument("-j", "--jobs", action="store", type=int, default=1,
                        help="Number of jobs to process in parallel. 0 (default) means serial processing.")
    parser.add_argument("-f", "--file", action="store", required=True,
                        help="Collision file(s) to process. Can contain glob wildcards.")
    parser.add_argument("-o", "--output", action="store", default="./",
                        help="Output path to store processed cascades.")
    parser.add_argument("-s", "--system", action="store", default="6H",
                        choices=["6H", "4H", "3C"],
                        help="The SiC polytype.")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
