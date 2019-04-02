import tweepy
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys
import time, datetime
style.use('ggplot')

def data_gen(t=0):
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
        yield t, np.sin(2*np.pi*t/5) * np.exp(-t/10.), np.cos(2*np.pi*t/5) * np.exp(-t/10.)

def init():
    ax[0].set_ylim(-1.1, 1.1)
    ax[0].set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    line2.set_data(xdata, ydata)
    return line, line2

fig, ax = plt.subplots(2,1)
line, = ax[0].plot([], [], lw=2)
line2, = ax[0].plot([], [], lw=2)
#ax[0][0].grid()
xdata, ydata, y2data = [], [], []


def run(data):
    # update the data
    t, y, y2 = data
    xdata.append(t)
    ydata.append(y)
    y2data.append(y2)
    xmin, xmax = ax[0].get_xlim()

    if t >= xmax:
        ax[0].set_xlim(xmin, 2*xmax)
        ax[0].figure.canvas.draw()
    line.set_data(xdata, ydata)
    line2.set_data(xdata, y2data)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()
