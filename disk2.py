import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import text

#Plots an even distribution of dots for a disk
def circle():
    n = int(input("Number of points?"))
    a = float(input("Initial Theta?"))
    b = float(input("Initial Phi?"))
    c = float(input("Angular difference?"))
    a=-0.5
    b=-0.5
    c=1
    radius = (1/2*c)*(np.sqrt(np.arange(1,n+1) / float(n+1)))

    golden_angle = np.pi * (3 - np.sqrt(5))
    theta = golden_angle * np.arange(1,n+1)

    points = np.zeros((n, 2))
    points[:, 0] = np.cos(theta)
    points[:, 1] = np.sin(theta)
    points *= radius.reshape((n, 1))
    x_points = []
    y_points = []
    for i in range(len(points)):
        x_points.append(points[i][0]+a+c/2)
        y_points.append(points[i][1]+b+c/2)
    fig, ax = plt.subplots()
    plt.plot(x_points,y_points,"b+")
    plt.xlim(a,a+c)
    plt.ylim(b,b+c)

    circle = plt.Circle((a+c/2,b+c/2),radius=c/2,color="k",alpha=0.3)
    ax.add_patch(circle)
    plt.xlabel("Θ")
    plt.ylabel("φ")
    text(0.1, 0.95,"N=" + str(n), ha='center', va='center', transform=ax.transAxes)
    plt.show()
    df = pd.DataFrame({"X":x_points,"Y":y_points})
    print(df)

#Calculates the center of mass for the N first iterations of circle(). It should tend to (0,0)
def center(number):
    xsum= []
    ysum = []
    for j in range (1,number):
        xsum.append(sum(circle(j)[0])/len(circle(j)[0]))
        ysum.append(sum(circle(j)[1]) / len(circle(j)[1]))
    plt.plot(xsum,ysum,"k+")
    for k in range(len(xsum)):
        plt.annotate(xy=(xsum[k],ysum[k]),text="N =" + str(k+1))
    plt.axhline(linestyle = "--", color = "r")
    plt.axvline(linestyle = "--", color = "r")
    plt.show()

circle()