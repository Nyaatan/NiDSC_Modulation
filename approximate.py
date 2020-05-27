import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fmin

import settings
from sysfun import full_plot


class Approximator:

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

    def _approximate(self):  # approximates signal to model function by minimizing cost function
        pars_start = np.array([np.random.uniform(0, 2*np.pi), 0])  # random first guess for minimizing function, uniform distribution
        m = fmin(self.Q, pars_start, args=(self.model, self.data,), disp=False)
        return m

    def approximate(self):  # approximates signal to QPSK by checking the signal flow in it's first quarter
        a = np.max(self.data[1])
        f = 0
        if self.rangex.size >= 4:
            bp = [self.data[1][0], self.data[1][self.rangex.size // 4]]
            if bp[0] < 0:
                if bp[1] < 0:
                    f = 3/4*np.pi
                else:
                    f = 5/4*np.pi
            else:
                if bp[1] >= 0:
                    f = 7/4*np.pi
                else:
                    f = 1/4*np.pi
        return f, a
