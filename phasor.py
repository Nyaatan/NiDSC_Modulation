from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np

import settings


class Phasor:
    def draw(self, value, mode='bpsk', title='', amplitude=1):
        if mode == 'bpsk':
            self._draw(value * np.pi, amplitude, title=title)
        elif mode == 'qpsk':
            if value == (1, 0):
                value = 1 / 4 * np.pi
            elif value == (0, 0):
                value = 3 / 4 * np.pi
            elif value == (0, 1):
                value = 5 / 4 * np.pi
            elif value == (1, 1):
                value = 7 / 4 * np.pi
            self._draw(value, amplitude, title=title)

    def _draw(self, value, amplitude, title=''):
        if not settings.plot:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.arrow(0, 0, np.cos(value) * amplitude, np.sin(value) * amplitude,
                 color='red', head_length=0.05, head_width=0.05,
                 length_includes_head=True)  # make arrow for given angle
        ax.spines['left'].set_position('center')  # --- properly
        ax.spines['bottom'].set_position('center')  # - show
        ax.spines['right'].set_color('none')  # ------- all
        ax.spines['top'].set_color('none')  # --------- axes
        plt.xlim(-1.5, 1.5)  # set axes limit for clear image
        plt.ylim(-1.5, 1.5)
        plt.title(title)
        fig.show()
        fig.savefig('plots/' + title + '.png')

    def draw_cloud(self, values, title=''):  # draws phasor cloud
        if not settings.plot:
            return

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for value in range(len(values['phase'])):
            self._add(values['phase'][value], ax, values['amplitude'][value], title=title)  # add arrows to phasor plot

        ax.spines['left'].set_position('center')  # --- properly
        ax.spines['bottom'].set_position('center')  # - show
        ax.spines['right'].set_color('none')  # ------- all
        ax.spines['top'].set_color('none')  # --------- axes
        plt.xlim(-1.5, 1.5)  # set axes limit for clear image
        plt.ylim(-1.5, 1.5)
        plt.title(title)
        fig.show()
        fig.savefig('plots/' + title + '.png')

    def _add(self, value, ax, amplitude, title=''):
        ax.arrow(0, 0, np.cos(value) * abs(amplitude), np.sin(value) * abs(amplitude),
                 color='red', head_length=0.05, head_width=0.05, length_includes_head=True)  # add arrow
