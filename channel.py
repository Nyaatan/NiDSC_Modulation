import sys

import numpy as np
import pyprind

import settings


class Channel:
    def send(self, signal, receiver):  # adds noise to signal and sends it to receiver
        receiver.receive(self.add_noise(signal, settings.amplitude_deviation, settings.phase_deviation))

    def add_noise(self, signal, amplitude=0.5, phase=30):
        """
        adds noise to signal by deviating each sample's amplitude and phase by a value generated randomly for each
        bit using normal distribution and given standard deviation of amplitude and phase
        """
        i = 0
        du = np.random.normal(0, amplitude)  # generate values of noise
        dfi = np.random.normal(0, phase)
        noised_signal = []
        bar = pyprind.ProgBar(signal.size, stream=sys.stdout)
        for sample in signal:
            i += 1
            if i % settings.fs == 0:  # if all samples of given bit are deviated, generate new values
                du = np.random.normal(0, amplitude)
                dfi = np.random.normal(0, phase)

            new_sample = du + np.cos(np.arccos(sample) + np.pi / 180 * dfi)  # add noise to sample
            noised_signal.append(new_sample)
            bar.update()
        return np.array(noised_signal)
