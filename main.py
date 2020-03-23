import numpy as np
from numpy.random.mtrand import rand

import phasor
import modulator as md
import matplotlib.pyplot as plt

mod = md.Modulator()
raw = [round(rand(), 0) for i in range(0, 12)]
a = np.array(raw)
x, y = mod.modulate_bpsk(a)
plt.plot(x, y)
plt.title('BPSK modulation')
plt.show()

ph = phasor.Phasor()
i = 0
for bit in raw:
    i+=1
    ph.draw(bit, mode='bpsk', title="BPSK. Bit no. %d" % i)

paired = [(raw[i], raw[i + 1])
          for i in range(len(raw)) if i % 2 == 0]

x, y = mod.modulate_qpsk(a)
plt.plot(x, y)
plt.title('QPSK modulation')
plt.show()
i = 0
for bit in paired:
    i+=1
    ph.draw(bit, mode='qpsk', title="QPSK. Bit no. %d" % i)
