"""
Created on Sun Mar  7 20:11:33 2021

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


#Load the file
url = ""
raw_data = pd.read_csv(url)
raw_data = raw_data[['Start Temperature (K)','End Temperature (K)','Scan','Position (cm)','Long Voltage','Long Scaled Response']] #filter out only useful columns


#Call this function to open the file in the browser
def open_file(dataFrame):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name+'.html'
    dataFrame.to_html(path)
    webbrowser.open("file://"+path)





#I used this when we had a problem at low temperatures: to extract the 5 scans of the first 3 temperatures
temporary_df = raw_data.head(64*15)
temperature_1 = temporary_df[0:320]
temperature_2 = temporary_df[320:640]
temperature_3 = temporary_df[640:]


#Call this function to separate the 5 scans for a given temperature
def separate_scans(df_input):
    scans_dict = {}
    for i in range(0,5):
        scans_dict[i+1] = df_input[df_input["Scan"]==(i+1)]
    return scans_dict
temp_1_scan_x = (separate_scans(temperature_1)[1])['Position (cm)'].values # x-axis values i.e. position in cm
temp_1_scan_1_y = (separate_scans(temperature_1)[1])['Long Voltage'].values
temp_1_scan_2_y = (separate_scans(temperature_1)[2])['Long Voltage'].values
temp_1_scan_3_y = (separate_scans(temperature_1)[3])['Long Voltage'].values
temp_1_scan_4_y = (separate_scans(temperature_1)[4])['Long Voltage'].values
temp_1_scan_5_y = (separate_scans(temperature_1)[5])['Long Voltage'].values
plt.figure('Temp_1')
plt.scatter(temp_1_scan_x,temp_1_scan_1_y)
plt.scatter(temp_1_scan_x,temp_1_scan_2_y)
plt.scatter(temp_1_scan_x,temp_1_scan_3_y)
plt.scatter(temp_1_scan_x,temp_1_scan_4_y)
plt.scatter(temp_1_scan_x,temp_1_scan_5_y)





#Convert field values to Tesla and rename the column to 'Field(T)'
raw_data['Field (Oe)'] = raw_data['Field (Oe)']/10000  # 1T = 10e+4 Oe
raw_data.rename(columns={"Field (Oe)":"Field(T)"}, inplace=True)


#Call this function with passing the required field value to return a sub-dataframe
def one_field_value(B_value):
    field_df = raw_data[raw_data["Field(T)"]==B_value]
    return field_df


B_2_df = one_field_value(2) #Data frame with one field value (can be implicitly passed to the scan-separating function in case the whole data frame is not needed)
B_2_dict = separate_scans(B_2_df) #Dictionary with the number of scan as key and corresponding dataframe as the value
B_3_df = one_field_value(3)
B_3_dict = separate_scans(B_3_df)
B_5_df = one_field_value(5)
B_5_dict = separate_scans(B_5_df)


#Call this function with scan number and pass also the dictionary to extract x and y values
def get_x_y (df_dict, n):
    scan_df = df_dict[n]
    x = scan_df['Position (cm)'].values
    y = scan_df['Long Scaled Response'].values
    return x,y


x_B2_1, y_B2_1 = get_x_y(B_2_dict, 1)
x_B2_3, y_B2_3 = get_x_y(B_2_dict, 3)


x_B3_1, y_B3_1 = get_x_y(B_3_dict, 1)
x_B3_4, y_B3_4 = get_x_y(B_3_dict, 4)


x_B5_1, y_B5_1 = get_x_y (B_5_dict, 1)
x_B5_5, y_B5_5 = get_x_y (B_5_dict, 5)





# Plotting 2 different scans for the same field value
plt.figure('B = 5T')
plt.scatter(x_B5_1, y_B5_1, label='Scan 1')
plt.scatter(x_B5_5, y_B5_5, label='Scan 5')
plt.title('2 different scans for B = 5T')
plt.xlabel('Position (cm)')
plt.ylabel('Long Voltage')
plt.legend(loc='best')
plt.show()





#Plotting 1 scan for 3 different field values
plt.figure('3 fields, 1 scan')
plt.scatter(x_B2_1, y_B2_1, label='B = 2T')
plt.scatter(x_B3_1, y_B3_1, label='B = 3T')
plt.scatter(x_B5_1, y_B5_1, label='B = 5T')
plt.xlabel('Position (cm)')
plt.ylabel('Long Voltage')
plt.legend(loc='best')
plt.show()
