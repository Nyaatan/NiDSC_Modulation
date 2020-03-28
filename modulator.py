import matplotlib.pyplot as plt
import numpy as np
from numpy.random.mtrand import rand


class Modulator:
    def __init__(self, fs=500, f=1):  # fs - sampling frequency, f - cosinusoide frequency
        self.fs = fs
        self.f = f

    def modulate_bpsk(self, signal):
        x = np.arange(self.fs, step=1 / self.fs)  # array of x axis points for which cosinus value will be calculated
        y = np.array([])                          # in each period
        for bit in signal:  # modulation of bits - cos(Ot) for 0 bit, cos(pi + Ot) for 1 bit
            print(bit)
            if bit == 0:
                y = np.append(y, np.cos(2 * np.pi * self.f * x / self.fs))
            else:
                y = np.append(y, np.cos(np.pi + 2 * np.pi * self.f * x / self.fs))
        x = np.linspace(0, signal.size * 2 * np.pi, y.size)  # create proper linear space for the plot
        return x, y

    def modulate_qpsk(self, signal):
        if signal.size % 2 != 0:  # make sure the signal can be paired
            signal = np.append(signal, 0)
        x = np.arange(self.fs, step=1 / self.fs)
        y = np.array([])
        paired = [(signal[i], signal[i + 1])
                  for i in range(len(signal)) if i % 2 == 0]  # pair the signal
        for pair in paired:  # modulate pairs - cos(1/4pi+Ot) for (1, 0), cos(3/4pi+Ot) for (0, 0),
            if pair == (1, 0):  # cos(5/4pi+Ot) for (0, 1), cos(7/4pi+Ot) for (1, 1)
                y = np.append(y, np.cos(1 / 4 * np.pi + np.pi * 2 * self.f * x / self.fs))
            elif pair == (0, 0):
                y = np.append(y, np.cos(3 / 4 * np.pi + np.pi * 2 * self.f * x / self.fs))
            elif pair == (0, 1):
                y = np.append(y, np.cos(5 / 4 * np.pi + np.pi * 2 * self.f * x / self.fs))
            elif pair == (1, 1):
                y = np.append(y, np.cos(7 / 4 * np.pi + np.pi * 2 * self.f * x / self.fs))
        x = np.linspace(0, signal.size * np.pi, y.size)
        return x, y


if __name__ == '__main__':  # for testing, runs when modulator.py is run
    a = np.array([round(rand(), 0) for i in range(0, 12)])
    mod = Modulator()
    x, y = mod.modulate_qpsk(a)
    plt.plot(x, y)
    plt.show()
