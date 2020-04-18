from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np

import settings


class Phasor:
    def draw(self, value, mode='bpsk', title=''):
        if mode == 'bpsk':
            self._draw(value*np.pi, title=title)
        elif mode == 'qpsk':
            if value == (1, 0):
                value = 1 / 4 * np.pi
            elif value == (0, 0):
                value = 3 / 4 * np.pi
            elif value == (0, 1):
                value = 5 / 4 * np.pi
            elif value == (1, 1):
                value = 7 / 4 * np.pi
            self._draw(value, title=title)

    def _draw(self, value, title=''):
        if not settings.plot:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.arrow(0, 0, np.cos(value), np.sin(value), color='red', head_length=0.1, head_width=0.1)  # make arrow for given angle
        ax.spines['left'].set_position('center')  # --- properly
        ax.spines['bottom'].set_position('center')  # - show
        ax.spines['right'].set_color('none')  # ------- all
        ax.spines['top'].set_color('none')  # --------- axes
        plt.xlim(-1.5, 1.5)  # set axes limit for clear image
        plt.ylim(-1.5, 1.5)
        plt.title(title)
        fig.show()
        fig.savefig('plots/'+title+'.png')

    def draw_cloud(self, values, title=''):  # draws phasor cloud
        if not settings.plot:
            return

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for value in values:
            self._add(value, ax, title=title)  # add arrows to phasor plot

        ax.spines['left'].set_position('center')  # --- properly
        ax.spines['bottom'].set_position('center')  # - show
        ax.spines['right'].set_color('none')  # ------- all
        ax.spines['top'].set_color('none')  # --------- axes
        plt.xlim(-1.5, 1.5)  # set axes limit for clear image
        plt.ylim(-1.5, 1.5)
        plt.title(title)
        fig.show()
        fig.savefig('plots/'+title+'.png')

    def _add(self, value, ax, title=''):
        ax.arrow(0, 0, np.cos(value), np.sin(value), color='red', head_length=0.1, head_width=0.1)  # add arrow
