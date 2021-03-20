import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df1 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/Pd_callibration/callibration_data_30K_hyst.rso.dat.csv",skiprows=30))
plt.scatter(df1["Field (Oe)"],df1["Long Moment (emu)"],s=10,c="r" ,label="First run")

plt.xlim([-10000,10000])
plt.ylim([-0.02,0.02])
plt.xlabel("Field (Oe)")
plt.ylabel("Long Moment (emu)")
X=df1[["Field (Oe)"]]
y=df1[["Long Moment (emu)"]]
regression = LinearRegression()
regression.fit(X,y)
y_pred = regression.predict(X)
plt.plot(X,y_pred,"k",label = "Regression")
plt.legend()
plt.show()