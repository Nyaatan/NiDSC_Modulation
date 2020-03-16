import matplotlib.pyplot as plt
import numpy as np


class Modulator:
    def __init__(self, fs=500, f=1):
        self.fs = fs
        self.f = f

    def modulate_bpsk(self, signal=np.array([])):
        x = np.arange(self.fs, step=1 / self.fs)
        y = np.array([])
        for bit in signal:
            print(bit)
            if bit == 0:
                y = np.append(y, np.cos(-1 / 2 * np.pi + 2 * np.pi * self.f * x / self.fs))
            else:
                y = np.append(y, -np.cos(-1 / 2 * np.pi + 2 * np.pi * self.f * x / self.fs))
        x = np.linspace(0, signal.size * 2 * np.pi, y.size)
        return x, y


if __name__ == '__main__':
    a = np.array([0, 1, 1, 0, 1, 1])
    mod = Modulator()
    plt.plot(mod.modulate_bpsk(a))

