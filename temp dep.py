import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

df1 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/Pd_callibration/callibration_data_tempDepend.rso.dat.csv",skiprows=30))
print(df1.columns)
plt.plot(df1["Temperature (K)"],df1["Long Moment (emu)"],"ko--", label="First run")


plt.xlabel("Temperature (K)")
plt.ylabel("Long Moment (emu)")
plt.legend()
plt.show()