import sys

import matplotlib.pyplot as plt
import numpy as np
import pyprind
from numpy.random.mtrand import rand


class Modulator:
    def __init__(self, fs=500, f=1):  # fs - sampling frequency, f - cosinusoide frequency
        self.fs = fs
        self.f = f

    def modulate_bpsk(self, signal):
        bar = pyprind.ProgBar(signal.size, stream=sys.stdout, title='Modulating BPSK')
        x = np.arange(0, 2*np.pi/self.f, step=2*np.pi/(self.fs*self.f))  # array of x axis points for which cosine will be calculated
        y = np.array([])   # in each period
        x = x[:self.fs]
        for bit in signal:  # modulation of bits - cos(Ot) for 0 bit, cos(pi + Ot) for 1 bit
            if bit == 0:
                y = np.append(y, np.cos(x*self.f))
            else:
                y = np.append(y, np.cos(np.pi + self.f*x))
            bar.update()
        x = np.linspace(0, signal.size * 2 * np.pi / self.f, y.size)  # create proper linear space for the plot
        return x, y

    def modulate_qpsk(self, signal):
        bar = pyprind.ProgBar(signal.size, stream=sys.stdout, title='Modulating QPSK')
        if signal.size % 2 != 0:  # make sure the signal can be paired
            signal = np.append(signal, 0)
        x = np.arange(0, 2*np.pi/self.f, step=2*np.pi/(self.fs*self.f))
        y = np.array([])
        paired = [(signal[i], signal[i + 1])
                  for i in range(len(signal)) if i % 2 == 0]  # pair the signal
        for pair in paired:  # modulate pairs - cos(1/4pi+Ot) for (1, 0), cos(3/4pi+Ot) for (0, 0),
            if pair == (1.0, 0.0):  # cos(5/4pi+Ot) for (0, 1), cos(7/4pi+Ot) for (1, 1)
                y = np.append(y, np.cos(1 / 4 * np.pi + x*self.f))
            elif pair == (0.0, 0.0):
                y = np.append(y, np.cos(3 / 4 * np.pi + x*self.f))
            elif pair == (0.0, 1.0):
                y = np.append(y, np.cos(5 / 4 * np.pi + x*self.f))
            elif pair == (1.0, 1.0):
                y = np.append(y, np.cos(7 / 4 * np.pi + x*self.f))
                bar.update()
        x = np.linspace(0, signal.size * 2 *np.pi/self.f, y.size)
        return x, y


if __name__ == '__main__':  # for testing, runs when modulator.py is run
    print(np.cos(np.pi/4))
    print(np.cos(3*np.pi/4))
    print(np.cos(5*np.pi/4))
    print(np.cos(7*np.pi/4))