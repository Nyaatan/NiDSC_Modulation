import sys

import numpy as np
import pyprind

import settings
from sysfun import full_plot


class Channel:
    def send(self, signal, receiver):  # adds noise to signal and sends it to receiver
        receiver.receive(self.add_noise(signal, settings.amplitude_deviation, settings.phase_deviation))

    def send_simple(self, signal, receiver):
        receiver.receive_simple(self.add_noise(signal, settings.amplitude_deviation, settings.phase_deviation,
                                               mode='simple'))

    def add_noise(self, signal, amplitude=0.5, phase=30, mode='realistic'):
        """
        adds noise to signal by deviating each sample's amplitude and phase by a value generated randomly for each
        bit using normal distribution and given standard deviation of amplitude and phase
        """
        if mode == 'realistic':
            i = 0
            du = np.random.normal(0, amplitude)  # generate values of noise
            dfi = np.random.normal(0, phase)
            noised_signal = np.array([])
            bar = pyprind.ProgBar(signal.size, stream=sys.stdout)
            x = np.arange(0, 2 * np.pi / settings.f, step=2 * np.pi / (settings.fs * settings.f))

            for i in range(signal.size//settings.fs):
                du = np.random.normal(0, amplitude)
                dfi = np.random.normal(0, phase)
                if signal[i*settings.fs] == 1 or signal[i*settings.fs] == -1:
                    f = np.arccos(signal[i*settings.fs])
                elif signal[i*settings.fs] < 0:
                    if signal[i*settings.fs+1] < signal[i*settings.fs]:
                        f = 3/4*np.pi
                    else:
                        f = 5/4*np.pi
                else:
                    if signal[i*settings.fs+1] < signal[i*settings.fs]:
                        f = 1/4*np.pi
                    else:
                        f = 7/4*np.pi
                new_sample = (1+du)*np.cos(np.pi/180 * dfi + f +
                                           x*settings.f)
                noised_signal = np.append(noised_signal, new_sample)
                bar.update()
            return np.array(noised_signal)
        elif mode == 'simple':
            result = {
                'phase': [],
                'amplitude': []
            }
            for i in range(signal.size//settings.fs):
                ph = np.random.normal(0, phase)
                result['amplitude'].append(signal[i*settings.fs]+np.random.normal(0, amplitude))
                if signal[i*settings.fs] == 1 or signal[i*settings.fs] == -1:
                    f = np.arccos(signal[i*settings.fs])
                elif signal[i*settings.fs] < 0:
                    if signal[i*settings.fs+1] < signal[i*settings.fs]:
                        f = 3/4*np.pi
                    else:
                        f = 5/4*np.pi
                else:
                    if signal[i*settings.fs+1] < signal[i*settings.fs]:
                        f = 1/4*np.pi
                    else:
                        f = 7/4*np.pi
                result['phase'].append(f+np.deg2rad(ph))
            return result
