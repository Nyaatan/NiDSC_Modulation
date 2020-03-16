import numpy as np
from numpy.random.mtrand import rand

import modulator as md
import matplotlib.pyplot as plt

mod = md.Modulator()
a = np.array([round(rand(), 0) for i in range(0, 12)])
x, y = mod.modulate_bpsk(a)
plt.plot(x, y)
plt.show()
