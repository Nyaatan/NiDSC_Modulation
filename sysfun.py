import os
import shutil
import json
from datetime import datetime
import matplotlib.pyplot as plt
from numpy.random.mtrand import rand


def log_err(msg):  # log error message to log.txt
    log_file = open('log.txt', 'a')
    log_msg = "[%s] %s\n" % (datetime.now().strftime("%d-%m-%Y %H:%M:%S"), msg)
    log_file.write(log_msg)


def rmkdir(path):
    if path in os.listdir():
        shutil.rmtree(path)  # remove previous path if exists, prevents Windows error "cannot create existing file"
    os.mkdir(path)  # create path directory


def json_load(path):
    return json.load(open(path))


def full_plot(x, y, title, path=None):
    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)  # create a figure and add plot
    ax.plot(x, y)  # plot modulated signal
    plt.title(title)
    fig.show()  # show the plot
    if path is not None:  # optionally save figure to path
        fig.savefig(path)


def load_signal(path, length=0, rand_fun=rand):
    # optionally allows to set custom pseudorandom function, numpy.random.mtrand.rand by default

    # generate pseudorandom signal rounded to {0,1} if no signal path is set
    if path is None:
        return [round(rand_fun(), 0) for i in range(0, length)]

    # load array of bits from JSON file if a signal path is set
    else:
        return json_load(path)
