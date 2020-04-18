import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fmin

import settings
from sysfun import full_plot


class Approximator():

    def __init__(self, data, mode):
        self.data = data
        self.rangex = data[0]
        self.mode = mode

    def model(self, x, phase):  # model function of approximated signal
        return np.cos(phase + x*settings.f)

    def Q(self, phase, model, data):  # cost function to minimize
        x, y = data
        ypred = model(x, phase)
        return sum((y - ypred) ** 2)

    def approximate(self):  # approximates signal to model function by minimizing cost function
        pars_start = np.random.uniform(0, 2*np.pi)  # random first guess for minimizing function, uniform distribution
        return fmin(self.Q, pars_start, args=(self.model, self.data,), disp=False)
