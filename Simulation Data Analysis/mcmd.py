import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns
import os
import statistics
from scipy.ndimage.filters import gaussian_filter
import time
pd.set_option('display.max_rows', 500)
start_time = time.time()

#mc_data_path = input("Path of Ar folder (MC)?")
mc_data_path = "C:/users/paduz/PycharmProjects/LAMMPS/Ar"
def last_chars(x):
    return(int(x[7:]))

df = pd.read_csv("C:/Users/paduz/PycharmProjects/LAMMPS/Ar/Ar_SiC_500/collisions.dat",skiprows=1)
df = df[df["Primary"] !=0]
UniqueType = df["Atom"].unique()
DataFrameDict = {elem: pd.DataFrame for elem in UniqueType}
for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df["Atom"] == key]

print(time.time() - start_time)
files_c_mc = DataFrameDict["C"]
files_si_mc = DataFrameDict["Si"]

#md_data_path = input("Name of the file")
md_data_path = "C:/Users/paduz/PycharmProjects/LAMMPS/clusters.csv"
md_data_path2 = "C:/Users/paduz/PycharmProjects/LAMMPS/clusters2.csv"
df = pd.DataFrame(pd.read_csv(md_data_path))
df2 = pd.DataFrame(pd.read_csv(md_data_path2))
files_si_mc = files_si_mc.rename(columns={"Atom":"PKA Type","Energy (eV)":"PKA Energy"})
files_c_mc = files_c_mc.rename(columns={"Atom":"PKA Type","Energy (eV)":"PKA Energy"})
df2 = df2[df2["PKA Energy"]>100]


mc = pd.concat([files_si_mc,files_c_mc])

mc["PKA Energy"] = mc["PKA Energy"].round()
mc = mc[mc["PKA Energy"]<=200]
md = pd.concat([df,df2])
md["tuple"] = list(zip(md["C_V"],md["C_I"],md["C_Si"],md["Si_V"],md["Si_I"],md["Si_C"]))
md = md.drop(columns=["PKA ID","PKA Theta","PKA Phi",'Si_V', 'Si_I', 'Si_C', 'C_V', 'C_I','C_Si',"Grid"])
md_si = md[md["tuple"] == (0,0,0,1,0,0)]
md_csi = md[md["tuple"] == (1,0,0,1,0,0)]


unique = sorted(md_si["PKA Energy"].unique())
unique.insert(0,0)
mc = mc.sort_values(["PKA Energy"],ascending=True)
mc["PKA Energy"] = pd.cut(mc["PKA Energy"], bins=unique,labels=unique[1::])
mc["Depth (nm)"] = pd.cut(mc["Depth (nm)"], bins =len(unique))
mc["Depth (nm)"] = [a.right for a in mc["Depth (nm)"]]


mc = mc.groupby(["Depth (nm)"])["PKA Energy"].agg(['unique']).reset_index()
md_si = md_si.groupby(["PKA Energy"]).sum().reset_index()

def1 = []

for i in range(len(mc["Depth (nm)"])):
    def2 = []
    for j in mc["unique"][i]:
        def2.append(md_si[md_si["PKA Energy"]==j]["Counts"].iloc[0])
    def1.append(sum(def2)/10000)

def1.insert(0,0)

b = [0]
b[1:] = mc["Depth (nm)"]

plt.plot(pd.Series(b), def1)
plt.xlim([0,10])
plt.ylim([0,1])
plt.show()
