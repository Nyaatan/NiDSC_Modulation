signal_length = 1000  # Length of generated pseudorandom signal (default: 12)
fs = 80  # sampling frequency of signal (default: 500)
f = 1  # frequency of cosine function (default: 1)
amplitude_deviation = 0.5  # standard deviation of amplitude noise (default: 0.5)
phase_deviation = 75  # standard deviation of phase noise (default: 30)

# turn modules on/off
only_bpsk = False  # Perform only bpsk modulation (default: False)
only_qpsk = False  # Perform only qpsk modulation (default: False)
only_simple = True  # perform only simple demodulation
only_realistic = False  # perform only realistic modulation
plot_phasors = False  # False to turn off plotting phasors (default: True)
save_plots = False  # False to disable saving plots (default: True)
plot = True  # Enable/Disable plotting graphs (default: True)

# paths
signal_path = None  # None to generate random signal or path to JSON file with list of bits (default: None)'
plot_dir = 'plots'  # Directory name for generating plots (default: 'plots')
bpsk_filename = '/BPSK modulation.png'  # filename to save BPSK modulation plot under (default: '/BPSK modulation.png')
qpsk_filename = '/QPSK modulation.png'  # filename to save QPSK modulation plot under (default: '/QPSK modulation.png')
qpsk_title = 'QPSK modulation'  # QPSK modulation plot title (default: 'QPSK modulation')
bpsk_title = 'BPSK modulation'  # BPSK modulation plot title (default: 'BPSK modulation')
phasor_title_qpsk = "QPSK. Bit pair no. %d - (%d, %d)"  # QPSK phasor plot title %[index, bit_0, bit_1] (default:
# "QPSK. Bit pair no. %d - (%d, %d)")
phasor_title_bpsk = "BPSK. Bit no. %d - %d"  # BPSK phasor plot title %[index, bit] (default: "BPSK. Bit no. %d - %d")
