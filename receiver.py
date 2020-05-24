import sys

import pyprind

from approximate import Approximator
from phasor import Phasor
from sysfun import *
import numpy as np


class Receiver:
    def __init__(self, mode):
        self.demodulated_signal = []
        self.signal = np.array([])
        self.received_signal = np.array([])
        self.x = 0
        self.mode = mode
        self.bits = []

    def receive(self, signal):  # save received signal
        self.received_signal = signal
        self.x = np.linspace(0, self.received_signal.size * 2 * np.pi, self.received_signal.size)

    def receive_simple(self, signal):
        self.signal = signal
        p = Phasor()
        p.draw_cloud(signal, title='Deviated bits phasor cloud - %s' % self.mode.upper())

    def demodulate_simple(self):
        bar = pyprind.ProgBar(len(self.signal['phase']), stream=sys.stdout, title='Demodulating (simple)...')
        for i in range(len(self.signal['phase'])):
            if self.mode is 'bpsk':
                for i in range(len(self.signal['phase'])):
                    bit = 0
                    if np.pi / 2 < self.signal['phase'][i] < 3 * np.pi / 2:
                        bit = 1
                    self.bits.append(bit)
                    bar.update()
            elif self.mode is 'qpsk':
                self.bits = []
                for i in range(len(self.signal['phase'])):
                    if 0 < self.signal['phase'][i] <= np.pi / 2:
                        bit = (1, 0)
                    elif np.pi / 2 < self.signal['phase'][i] <= np.pi:
                        bit = (0, 0)
                    elif np.pi < self.signal['phase'][i] <= 3 * np.pi / 2:
                        bit = (0, 1)
                    else:
                        bit = (1, 1)
                    self.bits.append(bit)
                    bar.update()

    def demodulate(self):  # demodulates received signal
        self.demodulated_signal = {
            'phase': [],
            'amplitude': []
        }
        self.signal = self.received_signal
        bar = pyprind.ProgBar(self.signal.size // settings.fs, stream=sys.stdout, title='Filtering...')
        for i in range(self.signal.size // settings.fs):
            # print('-' * 20, '\n', np.arccos(self.signal[settings.fs * i:settings.fs * (i + 1)]), np.max(self.signal[settings.fs * i:settings.fs * (i + 1)]))
            ap = Approximator((np.linspace(i * 2 * np.pi / settings.f, (i + 1) * 2 * np.pi / settings.f, settings.fs),
                               self.signal[settings.fs * i:settings.fs * (i + 1)]), self.mode)
            # splits signal into bit parts and approximates the phase shift value to determine value of bit
            approx = ap.approximate()
            approx_phase = (approx[0] % (2 * np.pi))  # normalize the result, just in case
            approx_ampl = approx[1]
            self.demodulated_signal['phase'].append(approx_phase)
            self.demodulated_signal['amplitude'].append(approx_ampl)
            bar.update()
        self.demodulated_signal['phase'] = np.array(self.demodulated_signal['phase'])
        self.demodulated_signal['amplitude'] = np.array(self.demodulated_signal['amplitude'])
        bar = pyprind.ProgBar(self.received_signal.size // settings.fs, stream=sys.stdout, title='Demodulating...')

        # determine bit's value based on approximated phase shift
        if self.mode is 'bpsk':
            for i in range(0, self.demodulated_signal['phase'].size):
                bit = 0
                if np.pi / 2 < self.demodulated_signal['phase'][i] < 3 * np.pi / 2:
                    bit = 1
                self.bits.append(bit)
                bar.update()

        # same, but in QPSK
        elif self.mode is 'qpsk':
            self.bits = []
            for i in range(0, self.demodulated_signal['phase'].size):
                if 0 < self.demodulated_signal['phase'][i] <= np.pi / 2:
                    bit = (1, 0)
                elif np.pi / 2 < self.demodulated_signal['phase'][i] <= np.pi:
                    bit = (0, 0)
                elif np.pi < self.demodulated_signal['phase'][i] <= 3 * np.pi / 2:
                    bit = (0, 1)
                else:
                    bit = (1, 1)
                self.bits.append(bit)
                bar.update()
