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

    def model(self, x, phase, a):  # model function of approximated signal
        return a * np.cos(phase + x*settings.f)

    def Q(self, args, model, data):  # cost function to minimize
        x, y = data
        phase, a = args
        ypred = model(x, phase, a)
        return sum((y - ypred) ** 2)

    def approximate(self):  # approximates signal to model function by minimizing cost function
        pars_start = np.array([np.random.uniform(0, 2*np.pi), np.random.uniform(0.5, 1)])  # random first guess for minimizing function, uniform distribution
        m = fmin(self.Q, pars_start, args=(self.model, self.data,), disp=False)
        return m
