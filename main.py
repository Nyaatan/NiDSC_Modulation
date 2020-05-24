import numpy as np
import csv
import modulator as md
import phasor
from approximate import Approximator
from channel import Channel
from receiver import Receiver
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
        phasor_title_qpsk = "QPSK. Bit pair no. %d - (%d, %d)"
        phasor_title_bpsk = "BPSK. Bit no. %d - %d"
        fs = 500
        f = 1


    log_err(dialogs["settings_not_found"])
    settings = Defaults()


def main():
    rmkdir(settings.plot_dir)  # make/remake plots directory

    mod = md.Modulator(settings.fs, settings.f)

    print(dialogs['sig_load'])
    raw = load_signal(settings.signal_path, settings.signal_length)  # create or load signal array (details in sysfun)

    a = np.array(raw)  # create a numpy array from raw bits
    ph = phasor.Phasor()
    channel = Channel()
    receiverB = Receiver('bpsk')
    receiverQ = Receiver('qpsk')
    modulated = {}
    bers = {}

    if not settings.only_qpsk:
        print(dialogs['modulating'] % "BPSK")
        x, y = mod.modulate_bpsk(a)  # modulate the signal
        modulated['bpsk'] = {
            'signal': y,
            'linspace': x
        }

        path = None
        if settings.save_plots:
            path = settings.plot_dir + settings.bpsk_filename

        print(dialogs['plotting'] % settings.bpsk_filename)
        full_plot(x, y, settings.bpsk_title, path=path)  # plot BPSK modulated signal

        i = 0
        if settings.plot_phasors:
            for bit in raw:  # plot phasors for every bit
                i += 1
                print(dialogs['plotting'] % settings.phasor_title_bpsk % (i, bit))
                ph.draw(bit, mode='bpsk', title=settings.phasor_title_bpsk % (i, bit))
        if not settings.only_realistic:
            print('Sending BPSK modulated signal to simple receiver')
            channel.send_simple(modulated['bpsk']['signal'], receiverB)
            print('Demodulating received BPSK signal (simple)')
            receiverB.demodulate_simple()

            err_bits = bit_errors(raw, receiverB.bits)
            bers['bpsk_raw'] = err_bits
            ber = BER(err_bits, settings.signal_length)  # calculate ber
            bers['bpsk'] = ber
            print("BPSK Incorrectly received bits (simple): %d" % err_bits)
            print("BPSK BER: %g" % ber)

        if not settings.only_simple:
            print(dialogs['sending'] % 'BPSK')
            channel.send(modulated['bpsk']['signal'], receiverB)  # send signal to receiver
            print(dialogs['plotting'] % "received BPSK signal")
            # plot received signal
            full_plot(modulated['bpsk']['linspace'], receiverB.received_signal, title='Received %s signal' % 'BPSK')

            print(dialogs['demodulating'] % "received BPSK")
            receiverB.demodulate()  # demodulate signal

            # print("Plotting phasor cloud...")
            # draw phasor cloud
            # ph.draw_cloud(receiverB.demodulated_signal, 'Received BPSK signal phasor cloud')

            err_bits = bit_errors(raw, receiverB.bits)
            bers['bpsk_raw'] = err_bits
            ber = BER(err_bits, settings.signal_length)  # calculate ber
            bers['bpsk'] = ber
            print("BPSK Incorrectly received bits: %d" % err_bits)
            print("BPSK BER: %g" % ber)

    if not settings.only_bpsk:
        if len(raw) % 2 is not 0:
            raw.append(0)  # make sure signal can be paired
            a = np.array(raw)

        paired = [(raw[i], raw[i + 1])
                  for i in range(len(raw)) if i % 2 == 0]  # pair bits for qpsk modulation

        print(dialogs['modulating'] % "QPSK")

        x, y = mod.modulate_qpsk(a)  # modulate the signal
        modulated['qpsk'] = {
            'signal': y,
            'linspace': x
        }

        path = None
        if settings.save_plots:
            path = settings.plot_dir + settings.qpsk_filename

        print(dialogs['plotting'] % settings.bpsk_filename)
        full_plot(x, y, settings.qpsk_title, path=path)

        i = 0
        if settings.plot_phasors:
            for bit in paired:  # plot phasors for every pair
                i += 1
                # print(dialogs['plotting'] % settings.phasor_title_qpsk % (i, bit))
                ph.draw(bit, mode='qpsk', title=settings.phasor_title_qpsk % (i, bit[0], bit[1]))

        if not settings.only_realistic:
            print('Sending QPSK modulated signal to simple receiver')
            channel.send_simple(modulated['qpsk']['signal'], receiverQ)
            print('Demodulating received QPSK signal (simple)')
            receiverQ.demodulate_simple()

            err_bits = bit_errors(paired, receiverQ.bits)
            bers['qpsk_raw'] = err_bits
            ber = BER(err_bits, settings.signal_length)  # calculate ber
            bers['qpsk'] = ber
            print("QPSK Incorrectly received bits (simple): %d" % err_bits)
            print("QPSK BER: %g" % ber)

        if not settings.only_simple:
            print(dialogs['sending'] % 'QPSK')
            channel.send(modulated['qpsk']['signal'], receiverQ)  # send signal to receiver
            print(dialogs['plotting'] % "received QPSK signal")
            # plot received signal
            full_plot(modulated['qpsk']['linspace'], receiverQ.received_signal, title='Received %s signal' % 'QPSK')

            print(dialogs['demodulating'] % "received QPSK")
            receiverQ.demodulate()  # demodulate signal

            # print("Plotting phasor cloud...")
            # ph.draw_cloud(receiverQ.demodulated_signal, 'Received QPSK signal phasor cloud')  # draw phasor cloud

            err_bits = bit_errors(paired, receiverQ.bits)
            bers['qpsk_raw'] = err_bits
            ber = BER(err_bits, settings.signal_length)  # calculate BER
            bers['qpsk'] = ber
            print("QPSK Incorrectly received bits: %d" % err_bits)
            print("QPSK BER: %g" % ber)

    log_result(bers)


main()
