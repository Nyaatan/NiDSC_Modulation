import sys

import numpy as np
import pyprind

import settings


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
                new_sample = (1+du)*np.cos(np.pi/180 * dfi + np.arccos(signal[i*settings.fs]) +
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
                result['amplitude'].append(signal[i*settings.fs]+np.random.normal(0, amplitude))
                result['phase'].append(np.arccos(signal[i*settings.fs])+np.pi / 180 *np.random.normal(0, phase))

            return result