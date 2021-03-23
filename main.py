import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

df1 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/SiC2/Hyst at 30K/SiC2_hyst_30K.rso.dat.csv", skiprows=30))
plt.plot(df1["Field (Oe)"],df1["Long Moment (emu)"],"ko--", label="First run")

'''df2 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/SiC 1/Hyst at 30K/Second measurement/SiC1_hyst_30K_2.rso.dat.csv",skiprows=30))
plt.plot(df2["Field (Oe)"],df2["Long Moment (emu)"],"ro--", label="Second run")'''
'''plt.xlim([-10000,10000])
plt.ylim([-0.00006,0.00006])'''
plt.xlabel("Field (Oe)")
plt.ylabel("Long Moment (emu)")
plt.legend()
plt.show()