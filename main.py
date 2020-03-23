import numpy as np
from numpy.random.mtrand import rand

import phasor
import modulator as md
import matplotlib.pyplot as plt
import settings
import json

length = settings.signal_length

mod = md.Modulator()
if settings.file_path is None:
    raw = [round(rand(), 0) for i in range(0, length)]  # generate pseudorandom signal
else:
    raw = json.load(settings.file_path)  # load array of bits from JSON file
a = np.array(raw)
ph = phasor.Phasor()

if not settings.only_qpsk:
    x, y = mod.modulate_bpsk(a)  # modulate the signal
    plt.plot(x, y)
    plt.title('BPSK modulation')
    plt.show()  # plot the signal

    i = 0
    for bit in raw:  # plot phasors for every bit
        i += 1
        ph.draw(bit, mode='bpsk', title="BPSK. Bit no. %d - %d" % (i, bit))

if not settings.only_bpsk:
    paired = [(raw[i], raw[i + 1])
              for i in range(len(raw)) if i % 2 == 0]  # pair bits for qpsk modulation

    x, y = mod.modulate_qpsk(a)  # modulate the signal
    plt.plot(x, y)
    plt.title('QPSK modulation')
    plt.show()  # plot the signal
    i = 0
    for bit in paired:  # plot phasors for every pair
        i += 1
        ph.draw(bit, mode='qpsk', title="QPSK. Bit pair no. %d - (%d, %d)" % (i, bit[0], bit[1]))
