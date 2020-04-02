import numpy as np

import modulator as md
import phasor
from sysfun import *

dialogs = json_load("dialogs.json")

try:
    import settings
except ModuleNotFoundError:
    class Defaults:  # default settings if file settings.py not found in working directory
        signal_length = 12
        only_bpsk = False
        only_qpsk = False
        signal_path = None
        plot_dir = 'plots'
        bpsk_filename = '/BPSK modulation.png'
        qpsk_filename = '/QPSK modulation.png'
        qpsk_title = 'QPSK modulation'
        bpsk_title = 'BPSK modulation'
        save_plots = True

    log_err(dialogs["settings_not_found"])
    settings = Defaults()

rmkdir(settings.plot_dir)  # make/remake plots directory

mod = md.Modulator()

raw = load_signal(settings.signal_path, settings.signal_length)  # create or load signal array (details in sysfun)

a = np.array(raw)  # create a numpy array from raw bits
ph = phasor.Phasor()

if not settings.only_qpsk:
    x, y = mod.modulate_bpsk(a)  # modulate the signal

    path = None
    if settings.save_plots:
        path = settings.plot_dir + settings.bpsk_filename

    full_plot(x, y, settings.bpsk_title, path=path)

    i = 0
    for bit in raw:  # plot phasors for every bit
        i += 1
        ph.draw(bit, mode='bpsk', title=settings.phasor_title_bpsk % (i, bit))

if not settings.only_bpsk:
    if len(raw) % 2 is not 0:
        raw.append(0)  # make sure signal can be paired
        a = np.array(raw)

    paired = [(raw[i], raw[i + 1])
              for i in range(len(raw)) if i % 2 == 0]  # pair bits for qpsk modulation

    x, y = mod.modulate_qpsk(a)  # modulate the signal

    path = None
    if settings.save_plots:
        path = settings.plot_dir + settings.qpsk_filename

    full_plot(x, y, settings.qpsk_title, path=path)

    i = 0
    for bit in paired:  # plot phasors for every pair
        i += 1
        ph.draw(bit, mode='qpsk', title=settings.phasor_title_qpsk % (i, bit[0], bit[1]))
