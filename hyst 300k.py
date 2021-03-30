import pandas as pd
import numpy as np
from scipy.ndimage import uniform_filter1d
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

route = input("File route?")
df1 = pd.DataFrame(pd.read_csv(route,skiprows=30))
plt.scatter(df1["Field (Oe)"],df1["Long Moment (emu)"],s=10,c="r" ,label="First run")
plt.xlim([-10000,10000])
plt.ylim([-0.00006,0.00006])
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
plt.clf()
y_new = [i[0] for i in y_pred]

new_m = [y["Long Moment (emu)"][i] - y_new[i] for i in range(len(X))]
plt.plot(X,new_m,"k+")
par = int(input(f"The number of points is: {len(new_m)}\n"
                f"Moving average parameter?"))
y_mean = uniform_filter1d(new_m,par)
for k in range(par):
    np.insert(y_mean,0,0)
plt.plot(X,y_mean,"r-")
plt.show()
