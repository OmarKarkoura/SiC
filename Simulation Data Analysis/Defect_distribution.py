import webbrowser
import pandas as pd
import numpy as np
import tempfile
import matplotlib.pyplot as plt
#import seaborn as sns
from scipy import optimize


# This code plots the defect distribution for one ion as a function of depth



def open_file(dataFrame):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name+'.html'
    dataFrame.to_html(path)
    webbrowser.open("file://"+path)





MC_url = "/Users/omarkarkoura/Library/Mobile Documents/com~apple~CloudDocs/Project:Thesis/Project/SImulation Analysis/Ar/Ar_SiC_5000/collisions.dat"
MC_df = pd.read_csv(MC_url,skiprows=1)
MC_df = MC_df[MC_df['Primary']==1]
MC_df = MC_df[MC_df['Atom']=='Si']
MC_df = MC_df[MC_df['Energy (eV)'] <= 200]
MC_df = MC_df.sort_values('Depth (nm)', ascending=True)
MC_df.drop('Atom',axis='columns',inplace=True)
MC_df['Primary'] = MC_df['Primary']/10000


MD_url = "/Users/omarkarkoura/Library/Mobile Documents/com~apple~CloudDocs/Project:Thesis/Project/SImulation Analysis/First Run/clusters.csv"
MD_df = pd.read_csv(MD_url)
MD_df.drop('Grid',axis='columns',inplace=True)
MD_df.drop('PKA ID',axis='columns',inplace=True)
MD_df.drop('PKA Theta',axis='columns',inplace=True)
MD_df.drop('PKA Phi',axis='columns',inplace=True)
MD_df["Tuple"] = list(zip(MD_df["Si_V"],MD_df["Si_I"],MD_df["Si_C"],MD_df["C_V"],MD_df["C_I"],MD_df["C_Si"]))
MD_df_SiV = MD_df[MD_df['Tuple']==(1,0,0,0,0,0)]
MD_df_SiV = MD_df_SiV.sort_values('PKA Energy',ascending=True)
MD_df_diV = MD_df[MD_df['Tuple']==(1,0,0,1,0,0)]
MD_df_diV = MD_df_diV.sort_values('PKA Energy',ascending=True)

#MD_df_total = MD_df[(MD_df['Tuple'] != (1,0,0,0,0,0)) and (MD_df['Tuple'] != (1,0,0,1,0,0))]






MC_df = MC_df[MC_df['Energy (eV)'] <= 200]
depth_bins = np.arange(0.5, 16, 0.5)
energy_bins = np.arange(MC_df.min(axis=0)['Energy (eV)'], 200.0, 5.0)
depth_labels = depth_bins[:-1]
energy_labels = energy_bins[:-1]
MC_df['depth_bin'] = pd.cut(MC_df['Depth (nm)'], bins=depth_bins, labels=depth_labels)
MC_df['energy_bin'] = pd.cut(MC_df['Energy (eV)'], bins=energy_bins, labels=energy_labels)

histogram = pd.DataFrame(columns=depth_labels, index=energy_labels)
histogram.update(pd.pivot_table(MC_df, index='energy_bin', columns='depth_bin',values='Primary', aggfunc=np.sum))
histogram = histogram.fillna(0)



MD_energy_list_SiV = MD_df_SiV['PKA Energy'].to_numpy()
MD_energy_list_diV = MD_df_diV['PKA Energy'].to_numpy()
MD_energy_list_total = MD_df['PKA Energy'].to_numpy()






counts_dict_total = {'0.5':0,'1.0':0, '1.5':0, '2.0':0,'2.5':0,'3.0':0,'3.5':0, '4.0':0, '4.5':0,'5.0':0,'5.5':0,'6.0':0,'6.5':0,'7.0':0,'7.5':0,'8.0':0,'8.5':0,'9.0':0,
'9.5':0,'10.0':0,'10.5':0,'11.0':0,'11.5':0,'12.0':0, '12.5':0, '13.0':0,'13.5':0,'14.0':0,'14.5':0,'15.0':0}

for MDIndex in range(len(MD_energy_list_total)):

    for depth_index in range(len(depth_labels)):

        for energy_index in range(len(energy_labels)):

            if energy_index ==0:

                if (MD_energy_list_total[MDIndex] >= energy_labels[0]) & (MD_energy_list_total[MDIndex]< energy_labels[1]):


                    counts_dict_total[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            elif energy_index == len(energy_labels)-1:
                if (MD_energy_list_total[MDIndex] <= energy_labels[energy_index]) & (MD_energy_list_total[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict_total[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            else:
                if (MD_energy_list_total[MDIndex]< energy_labels[energy_index]) & (MD_energy_list_total[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict_total[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue




counts_dict = {'0.5':0,'1.0':0, '1.5':0, '2.0':0,'2.5':0,'3.0':0,'3.5':0, '4.0':0, '4.5':0,'5.0':0,'5.5':0,'6.0':0,'6.5':0,'7.0':0,'7.5':0,'8.0':0,'8.5':0,'9.0':0,
'9.5':0,'10.0':0,'10.5':0,'11.0':0,'11.5':0,'12.0':0, '12.5':0, '13.0':0,'13.5':0,'14.0':0,'14.5':0,'15.0':0}

for MDIndex in range(len(MD_energy_list_SiV)):

    for depth_index in range(len(depth_labels)):

        for energy_index in range(len(energy_labels)):

            if energy_index ==0:

                if (MD_energy_list_SiV[MDIndex] >= energy_labels[0]) & (MD_energy_list_SiV[MDIndex]< energy_labels[1]):


                    counts_dict[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            elif energy_index == len(energy_labels)-1:
                if (MD_energy_list_SiV[MDIndex] <= energy_labels[energy_index]) & (MD_energy_list_SiV[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            else:
                if (MD_energy_list_SiV[MDIndex]< energy_labels[energy_index]) & (MD_energy_list_SiV[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue

counts_dict_2 = {'0.5':0,'1.0':0, '1.5':0, '2.0':0,'2.5':0,'3.0':0,'3.5':0, '4.0':0, '4.5':0,'5.0':0,'5.5':0,'6.0':0,'6.5':0,'7.0':0,'7.5':0,'8.0':0,'8.5':0,'9.0':0,
'9.5':0,'10.0':0,'10.5':0,'11.0':0,'11.5':0,'12.0':0, '12.5':0, '13.0':0,'13.5':0,'14.0':0,'14.5':0,'15.0':0}

for MDIndex in range(len(MD_energy_list_diV)):

    for depth_index in range(len(depth_labels)):

        for energy_index in range(len(energy_labels)):

            if energy_index ==0:

                if (MD_energy_list_diV[MDIndex] >= energy_labels[0]) & (MD_energy_list_diV[MDIndex]< energy_labels[1]):


                    counts_dict_2[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            elif energy_index == len(energy_labels)-1:
                if (MD_energy_list_diV[MDIndex] <= energy_labels[energy_index]) & (MD_energy_list_diV[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict_2[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue
            else:
                if (MD_energy_list_diV[MDIndex]< energy_labels[energy_index]) & (MD_energy_list_diV[MDIndex]>= energy_labels[energy_index-1]):

                    counts_dict_2[str(depth_labels[depth_index])]+= (histogram.loc[(energy_labels[energy_index]),(depth_labels[depth_index])])
                else:
                    #counts_dict[str(depth_labels[depth_index])].append(0)
                    continue





counts_list_SiV = []
counts_list_diV = []
counts_list_total = []
for key in counts_dict.keys():
    counts_list_SiV.append(counts_dict[key]/120)
for key in counts_dict_2.keys():
    counts_list_diV.append(counts_dict_2[key]/120)
for key in counts_dict_total.keys():
    counts_list_total.append(counts_dict_total[key]/120)
plt.figure()
plt.title('Defect distribution for Ar ion at 5000 eV')
plt.ylabel('Defects/ion')
plt.xlabel('Depth (nm)')
plt.grid()
plt.plot(depth_labels,counts_list_SiV,label='Si-V')
plt.plot(depth_labels,counts_list_diV,label='di-V')
plt.plot(depth_labels,counts_list_total, label='Total')
plt.legend(loc='best')
plt.show()


#Ignore
'''fig, ax = plt.subplots()
ax.set_aspect("equal")
#plt.axis([0, histogram.])
ax.pcolormesh(histogram)
ax.set_yticks(np.arange(histogram.shape[0])[::5] + 0.5, minor=False)
ax.set_xticks(np.arange(histogram.shape[1])[::5] + 0.5, minor=False)
ax.set_xticklabels(histogram.columns[::5], minor=False)
ax.set_yticklabels(histogram.index[::5], minor=False)
ax.set_xlabel("Depth (nm)")
ax.set_ylabel("Energy (eV)")
plt.show()'''
