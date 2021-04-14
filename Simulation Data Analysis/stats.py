import pandas as pd
import matplotlib.pyplot as plt
import time
start_time = time.time()
pd.set_option('display.max_columns', 150)

file = input("File path?")
df = pd.DataFrame(pd.read_csv(file))
number_greatest = int(input("Number of defects to plot?"))
df["tuple"] = list(zip(df["C_V"],df["C_I"],df["C_Si"],df["Si_V"],df["Si_I"],df["Si_C"]))
df["total"] = 1


df = df[["PKA Type","PKA Energy","tuple","Counts","total",'PKA ID', 'Grid','PKA Theta', 'PKA Phi',
       'Si_V', 'Si_I', 'Si_C', 'C_V', 'C_I', 'C_Si']]
fig, (ax1, ax2) = plt.subplots(1, 2)

df = df.groupby(["PKA Type","PKA Energy","tuple"]).sum().reset_index()
df["Counts"] = df["Counts"]/120
df = df.sort_values(by=["PKA Type","tuple","PKA Energy"])


UniqueType = df["PKA Type"].unique()
DataFrameDict = {elem : pd.DataFrame for elem in UniqueType}
for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df["PKA Type"] == key]


UniqueTuple_C = DataFrameDict["C"]["tuple"].unique()
greaters_c = DataFrameDict["C"].groupby(["tuple"]).sum().reset_index().sort_values(by=["Counts"],ascending=False)["tuple"].unique()
greaters_c = greaters_c[:number_greatest]

DataFrameDict_C = {elem_c : pd.DataFrame for elem_c in UniqueTuple_C}
c_dict = {}
for key in greaters_c:
    c_dict[key] = DataFrameDict["C"][:][DataFrameDict["C"]["tuple"] == key]

UniqueTuple_Si = DataFrameDict["Si"]["tuple"].unique()
greaters_si = DataFrameDict["Si"].groupby(["tuple"]).sum().reset_index().sort_values(by=["Counts"],ascending=False)["tuple"].unique()
greaters_si = greaters_si[:number_greatest]
DataFrameDict_Si = {elem_si : pd.DataFrame for elem_si in UniqueTuple_Si}
si_dict = {}
for key in greaters_si:
    si_dict[key] = DataFrameDict["Si"][:][DataFrameDict["Si"]["tuple"] == key]

for i in greaters_c:
    ax1.plot(c_dict[i]["PKA Energy"],c_dict[i]["Counts"],label = f"{i}")
for j in greaters_si:
    ax2.plot(si_dict[j]["PKA Energy"], si_dict[j]["Counts"],label = f"{j}")

ax1.set_xlabel("Energy (eV)")
ax2.set_xlabel("Energy (eV)")
ax1.set_ylabel("Count")
ax2.set_ylabel("Count")
ax1.title.set_text("C PKA defect")
ax2.title.set_text("Si PKA defect")
ax1.legend(bbox_to_anchor=(-0.1, 0.6))
ax2.legend(bbox_to_anchor=(1, 0.6))
plt.show()
