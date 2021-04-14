import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns
import os
from scipy.ndimage.filters import gaussian_filter

path = input("Path?")

def last_chars(x):
    return(int(x[7:]))

for i in sorted(os.listdir(path),key=last_chars):
    df = pd.read_csv(f"{path}/{i}/collisions.dat", skiprows=1)
    df = df[df["Primary"] !=0]
    UniqueType = df["Atom"].unique()
    DataFrameDict = {elem: pd.DataFrame for elem in UniqueType}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df["Atom"] == key]

files_c = DataFrameDict["C"]
files_c = files_c.rename(columns = {"Primary":"Count"})
files_c["Count"] = files_c["Count"]
files_si = DataFrameDict["Si"]
files_si = files_si.rename(columns = {"Primary":"Count"})
files_si["Count"] = files_si["Count"]

fig, (ax1, ax2) = plt.subplots(1, 2)

hist_c = ax1.hist2d(files_c["Depth (nm)"], files_c["Energy (eV)"], bins=(50, 1000), cmap=plt.cm.magma)
hist_si = ax2.hist2d(files_si["Depth (nm)"], files_si["Energy (eV)"], bins=(50, 1000), cmap=plt.cm.magma)

cbar_c = plt.colorbar(hist_c[3],ax=ax1)
cbar_c_ticks = [i/10000 for i in cbar_c.get_ticks()]
cbar_c.ax.set_yticklabels(cbar_c_ticks)

cbar_si = plt.colorbar(hist_si[3], ax=ax2)
cbar_si_ticks = [i/10000 for i in cbar_si.get_ticks()]
cbar_si.ax.set_yticklabels(cbar_si_ticks)


ax1.set_ylim(25,200)
ax2.set_ylim(40,200)
ax1.title.set_text("C PKA defect")
ax2.title.set_text("Si PKA defect")
ax1.set_xlabel("Depth (nm)")
ax2.set_xlabel("Depth (nm)")
ax1.set_ylabel("PKA Energy (eV)")
ax2.set_ylabel("PKA Energy (eV)")
plt.show()



"""fig, (ax1, ax2) = plt.subplots(1, 2)
dfc_smooth = gaussian_filter(files_c, sigma=1)
ax1.set_facecolor('black')
ax2.set_facecolor('black')
dfsi_smooth = gaussian_filter(files_si, sigma=1)
sns.heatmap(dfc_smooth,ax =ax1).invert_yaxis()
ax1.set_ylim(0,200)
sns.heatmap(dfsi_smooth, ax=ax2).invert_yaxis()
ax2.set_ylim(0,200)
ax1.title.set_text("C PKA defect")
ax2.title.set_text("Si PKA defect")"""



plt.show()
