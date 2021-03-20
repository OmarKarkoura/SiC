import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df1 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/SiC 1/Hyst at 30K/First measurement/SiC1_hyst_30K.rso.dat.csv",skiprows=30))
plt.scatter(df1["Field (Oe)"],df1["Long Moment (emu)"],s=6,c="b", label="First run")

df2 = pd.DataFrame(pd.read_csv("C:/users/paduz/PycharmProjects/SiC/SiC 1/Hyst at 30K/Second measurement/SiC1_hyst_30K_2.rso.dat.csv",skiprows=30))
plt.scatter(df2["Field (Oe)"],df2["Long Moment (emu)"],s=6,c="r" ,label="Second run")
plt.xlim([-10000,10000])
plt.ylim([-0.00006,0.00006])
plt.xlabel("Field (Oe)")
X=df1[["Field (Oe)"]]
y=df1[["Long Moment (emu)"]]
regression = LinearRegression()
regression.fit(X,y)
y_pred = regression.predict(X)
plt.plot(X,y_pred,"k",label = "Regression")

plt.ylabel("Long Moment (emu)")
plt.legend()
plt.show()