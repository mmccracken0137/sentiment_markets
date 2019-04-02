# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
#
# fig, ax = plt.subplots()
# xdata, ydata = [], []
# ln, = plt.plot([], [], 'ro')
#
# def init():
#     ax.set_xlim(0, 2*np.pi)
#     ax.set_ylim(-1, 1)
#     return ln,
#
# def update(frame):
#     xdata.append(frame)
#     ydata.append(np.sin(frame))
#     ln.set_data(xdata, ydata)
#     return ln,
#
# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen(t=0):
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.), np.cos(2*np.pi*t) * np.exp(-t/10.)


def init():
    ax[0][0].set_ylim(-1.1, 1.1)
    ax[0][0].set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    line2.set_data(xdata, ydata)
    return line, line2

fig, ax = plt.subplots(2,2)
line, = ax[0][0].plot([], [], lw=2)
line2, = ax[0][0].plot([], [], lw=2)
ax[0][0].grid()
xdata, ydata, y2data = [], [], []


def run(data):
    # update the data
    t, y, y2 = data
    xdata.append(t)
    ydata.append(y)
    y2data.append(y2)
    xmin, xmax = ax[0][0].get_xlim()

    if t >= xmax:
        ax[0][0].set_xlim(xmin, 2*xmax)
        ax[0][0].figure.canvas.draw()
    line.set_data(xdata, ydata)
    line2.set_data(xdata, y2data)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()
