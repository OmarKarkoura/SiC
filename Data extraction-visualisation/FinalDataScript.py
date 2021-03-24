"""
Created on Sun Mar  7 21:25:13 2021

@author: Omar Karkoura
"""
#useful packages to facilitate extraction/visualisation of the data
import webbrowser
import pandas as pd
import numpy as np
import tempfile
import matplotlib.pyplot as plt
from scipy import optimize


#Note: I manually remove the description in the header and also convert it to a csv
#For better readability: related blocks of code are separated by 2 line breaks, unrelated blocks are separated by 5 line breaks


def open_file(dataFrame):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name+'.html'
    dataFrame.to_html(path)
    webbrowser.open("file://"+path)





url_30K = ""
url_300K = ""
url_tempDepend = ""
pd_30K_url = ""    # I use the data in this file for performing corrections


pd_30K = pd.read_csv(pd_300K_url)
pd_30K = pd_300K[["Time", "Field (Oe)", "Temperature (K)", "Long Moment (emu)", "Long Scan Std Dev"]]  # Filter out only useful columns


pd_30K['Field (Oe)'] = pd_300K['Field (Oe)']/10000
pd_30K.rename(columns={"Field (Oe)":"Field(T)"}, inplace=True)





# In the following, I use this linear function (simply m*x where m is the slope) to subtract the line from the callibration data such that we can get information about the actual field
def linear_func(x,m):
    return m*x


params, params_covariance = optimize.curve_fit(linear_func, pd_30K['Field(T)'], pd_30K['Long Moment (emu)'])  #Getting the fitting parameters (i.e the slope)
pd_newData = pd_30K['Long Moment (emu)'] - params[0]*pd_30K['Field(T)']   # Subtracting the line
pd_correction = pd_30K['Long Moment (emu)']/params[0]  # Values of actual field


# Plotting the data with the fitted line
plt.figure('Callibration')
plt.title('Fitting function for the data points of Pd at 30K')
plt.plot(pd_300K['Field(T)'], linear_func(pd_300K['Field(T)'], params[0]), label='Fitted function')
plt.plot(pd_300K['Field(T)'], pd_300K['Long Moment (emu)'], label='Data points')
plt.show()





data_30K = pd.read_csv(url_30K)
data_300K = pd.read_csv(url_300K)
data_tempDepend = pd.read_csv(url_tempDepend)


data_30K = data_30K[["Time", "Field (Oe)", "Temperature (K)", "Long Moment (emu)", "Long Scan Std Dev"]]
data_300K = data_300K[["Time", "Field (Oe)", "Temperature (K)", "Long Moment (emu)", "Long Scan Std Dev"]]
data_tempDepend = data_tempDepend[["Time", "Field (Oe)", "Temperature (K)", "Long Moment (emu)", "Long Scan Std Dev"]]


data_30K['Field (Oe)'] = data_30K['Field (Oe)']/10000
data_30K.rename(columns={"Field (Oe)":"Field(T)"}, inplace=True)
data_300K['Field (Oe)'] = data_300K['Field (Oe)']/10000
data_300K.rename(columns={"Field (Oe)":"Field(T)"}, inplace=True)





# Plotting the temperature dependence curve
plt.figure('Temperature Dependence')
plt.scatter(data_tempDepend['Temperature (K)'], data_tempDepend['Long Moment (emu)'])
plt.show()


# Plotting data at 30K
plt.figure('30K')
plt.scatter(data_30K['Field(T)'], data_30K['Long Moment (emu)'], label='Data at 30K')
plt.title('Magnetic moment dependence on field at 30K')
plt.xlabel('Field (T)')
plt.ylabel('Long Magnetic Moment (emu)')
plt.ylim(-0.00029,0.00029)
plt.legend(loc='best')
plt.show()


#Comparing data at 30K & 300K. Moreover I have included in the same figure the observed ferromagnetic loop at 300K (should be zoomed by hand)
fig, ax = plt.subplots(2,1)
fig.tight_layout()
ax[0].scatter(data_300K['Field(T)'],data_300K['Long Moment (emu)'],label='300K')
ax[0].scatter(data_30K['Field(T)'],data_30K['Long Moment (emu)'],label='30K')
ax[0].set_ylim(-0.00029,0.00029)
ax[0].set_title('Magnetic moment dependence on field at two different temperatures')
ax[0].set_xlabel('Field (T)')
ax[0].set_ylabel('Long Magnetic Moment (emu)')
ax[0].legend(loc='best')

ax[1].scatter(data_300K['Field(T)'],data_300K['Long Moment (emu)'],label='300K')
ax[1].set_xlabel('Field (T)')
ax[1].set_ylabel('Long Magnetic Moment (emu)')
ax[1].set_title('Observed Ferromagnetic behavior at 300K')
ax[1].set_ylim(-0.00029,0.00029)
ax[1].legend(loc='best')
plt.show()





#Subtracting the line from the SiC data using the set and then actual field from callibration data for corrections comparison
params_setB, params_setB_covariance = optimize.curve_fit(linear_func, data_30K['Field(T)'], data_30K['Long Moment (emu)'])
setB_lineSubtracted = data_30K['Long Moment (emu)'] - params_setB[0]*data_30K['Field(T)']
params_actualB, params_actualB_covariance = optimize.curve_fit(linear_func, pd_correction, data_30K['Long Moment (emu)'])
actualB_lineSubtracted = data_30K['Long Moment (emu)'] - params_actualB[0]*pd_correction


#Plotting the data at 30K for the set and actual fields for comparison
fig, ax = plt.subplots(2,1)
fig.tight_layout()
ax[0].scatter(pd_correction, final_data_30K['Long Moment (emu)'],label='Actual Field')
ax[0].set_xlabel('Field (T)')
ax[0].set_ylabel('Long Magnetic Moment (emu)')
ax[0].legend(loc='best')

ax[1].scatter(final_data_30K['Field(T)'], final_data_30K['Long Moment (emu)'], color='black', label='Set Field')
ax[1].set_xlabel('Field (T)')
ax[1].set_ylabel('Long Magnetic Moment (emu)')
ax[1].legend(loc='best')
plt.show()


#Plotting the subtracted lines at 30K for the set and actual fields for comparison (better for understanding/observing corrections than the previous plot)
fig, ax = plt.subplots(2,1)
fig.tight_layout()
ax[0].scatter(pd_correction, actualB_lineSubtracted,label='Actual Field')
ax[0].set_xlabel('Field (T)')
ax[0].set_ylabel('Long Magnetic Moment (emu)')
ax[0].legend(loc='best')

ax[1].scatter(data_30K['Field(T)'], setB_lineSubtracted, color='black', label='Set Field')
ax[1].set_xlabel('Field (T)')
ax[1].set_ylabel('Long Magnetic Moment (emu)')
ax[1].legend(loc='best')
plt.show()
