import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import random
import math

def disk(m, n , iter):
    x_th = []
    y_th = []
    distance_min = 10000
    for i in range(m):
        x_th.append(random.uniform(0, 1))
        y_th.append(random.uniform(0, 1))
    for t in range(iter):
        x = []
        y = []
        distance_mean = 0
        distance = []
        for j in range(n):
            x.append(random.uniform(0,1))
            y.append(random.uniform(0,1))
        for k in range(n):
            for l in range(m):
                distance.append(math.sqrt((x[k] - x_th[l]) ** 2 + (y[k] - y_th[l]) ** 2))
        distance_mean = sum(distance) / len(distance)
        if distance_mean <= distance_min:
            distance_min = distance_mean
            x_max = x
            y_max = y
    plt.plot(x_max,y_max,"k+")
    plt.plot(x_th,y_th,"r+",alpha=0.25)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.show()
    data = {"X" : x_max , "Y" : y_max}
    print(pd.DataFrame(data , columns=["X","Y"]))



def disk2(m,number,points):
    x_th = []
    y_th = []
    for i in range(m):
        x_th.append(random.uniform(0, 1))
        y_th.append(random.uniform(0, 1))

    x_np = np.linspace(0,1,number)
    y_np = np.linspace(0,1,number)
    x_1, y_1 = np.meshgrid(x_np, y_np)
    L = {}
    for q in range(number):
        for w in range(number):
            L[(x_1[0][q], y_1[w][0])] = 0
    for t in range(number):
        for o in range(number):
            for j in range(m):
                if math.sqrt((x_1[0][t] - x_th[j]) ** 2 + (y_1[o][0] - y_th[j]) ** 2) < (1/(2*(number+1))):
                    L[(x_1[0][t],y_1[o][0])] +=1
    L = sorted(L, key=L.get,reverse=True)
    xplot = []
    yplot= []
    for u in range(len(L)):
        xplot.append(L[u][0])
        yplot.append(L[u][1])
    plt.plot(xplot[:points],yplot[:points], "r+")
    plt.plot(x_th,y_th,"k+",alpha=0.05)
    plt.xlabel("Θ")
    plt.ylabel("φ")
    plt.show()
disk2(100000,20,10)
