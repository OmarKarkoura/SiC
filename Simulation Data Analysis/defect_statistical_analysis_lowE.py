import numpy as np
import pandas as pd
import matplotlib.pyplot as plt





pd.set_option('display.max_columns', 150)





df = pd.DataFrame(pd.read_csv(""))
df["tuple"] = list(zip(df["C_V"],df["C_I"],df["C_Si"],df["Si_V"],df["Si_I"],df["Si_C"]))
df["total"] = 1
df.drop(["PKA ID","Grid","PKA Theta","PKA Phi"],axis=1, inplace=True)
df = df[["PKA Type","PKA Energy","tuple","Counts","total"]]
df = df.groupby(["PKA Type","PKA Energy","tuple"]).sum().reset_index()
df["Counts"] = df["Counts"]/120
#df = df.sort_values(by=["PKA Type","tuple","PKA Energy"])





fig, (ax1, ax2) = plt.subplots(1, 2)





UniqueType = df["PKA Type"].unique()
DataFrameDict = {elem : pd.DataFrame for elem in UniqueType}
for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df["PKA Type"] == key]





UniqueTuple_C = DataFrameDict["C"]["tuple"].unique()
DataFrameDict_C = {elem_c : pd.DataFrame for elem_c in UniqueTuple_C}
for key in list(DataFrameDict_C.keys()):
    DataFrameDict_C[key] = DataFrameDict["C"][:][DataFrameDict["C"]["tuple"] == key]


UniqueTuple_Si = DataFrameDict["Si"]["tuple"].unique()
DataFrameDict_Si = {elem_si : pd.DataFrame for elem_si in UniqueTuple_Si}
for key in list(DataFrameDict_Si.keys()):
    DataFrameDict_Si[key] = DataFrameDict["Si"][:][DataFrameDict["Si"]["tuple"] == key]





def labelFunc(tuple_list):
    label_dict = {0:'Si_V', 1:'Si_I', 2:'Si_C', 3:'C_V', 4:'C_I', 5:'C_Si'}
    names_list = []
    return_string = ''
    for i in label_dict.keys():
        if tuple_list[i] != 0:
            names_list.append(str(tuple_list[i])+label_dict[i])
    if names_list.count == 1:
        return_string = names_list[0]
    else:
        for i in range(len(names_list)):
            if return_string == '':
                return_string = names_list[0]
            else:
                return_string = return_string + ',' + names_list[i]
    return return_string


for i in UniqueTuple_C:
    ax1.plot(DataFrameDict_C[i]["PKA Energy"],DataFrameDict_C[i]["Counts"],label = labelFunc(i))
for j in UniqueTuple_Si:
    ax2.plot(DataFrameDict_Si[j]["PKA Energy"], DataFrameDict_Si[j]["Counts"],label = labelFunc(j))


ax1.set_xlabel("Energy (eV)")
ax2.set_xlabel("Energy (eV)")
ax1.set_ylabel("Count")
ax2.set_ylabel("Count")
ax1.title.set_text("C PKA defect")
ax2.title.set_text("Si PKA defect")
ax1.legend(bbox_to_anchor=(-0.05, 1))
ax2.legend(bbox_to_anchor=(1.01, 1))
plt.savefig("test.png")
plt.show()
