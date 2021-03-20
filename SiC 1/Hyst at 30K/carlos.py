import numpy as np
import matplotlib.pyplot as plt

I = np.linspace(0,1,1000)
L=[]
J=[]
for j in I:
    for k in np.linspace(-10,10,10000):
        if round(k/2,2) == round(j*(1+(4/3)*k**2)**2,2):
            L.append(k)
            J.append(1)
        else:
            J.append(0)
    print(len(L))
plt.plot(L)
plt.plot(J,"r")
plt.show()