import matplotlib.pyplot as plt
import numpy as np


def generate_sinusoidal_wave(f):
    T = 1/f
    return np.sin(2*np.pi*f*np.arange(0, 3*T, 1/(100.0*f)))


def generate_partial_wave(signals):
    number_of_signals = len(signals)
    result = []
    n = 0
    for signal in signals:
        n += len(signal)

    signal_num = 0
    i = 0
    while signal_num < number_of_signals:
        while i < len(signals[signal_num])//number_of_signals:
            result.append(signals[signal_num][i])
            i += 1
        signal_num += 1
    return result


signal1 = generate_sinusoidal_wave(100)
signal2 = generate_sinusoidal_wave(200)
signal3 = generate_sinusoidal_wave(300)
signal4 = generate_sinusoidal_wave(400)
signal5 = generate_sinusoidal_wave(500)

min_len = min([len(signal1), len(signal2), len(signal3), len(signal4), len(signal5)])

signal1 = signal1[:min_len]
signal2 = signal2[:min_len]
signal3 = signal3[:min_len]
signal4 = signal4[:min_len]
signal5 = signal5[:min_len]

signals = [signal1, signal2, signal3, signal4, signal5]

summed_signal = signal1 + signal2 + signal3 + signal4 + signal5
partial_signal = generate_partial_wave(signals)

# plot summed signal

summed_signal_FFT = np.fft.fft(summed_signal)
real_part = np.real(summed_signal_FFT)
imaginary_part = np.imag(summed_signal_FFT)

plt.plot(real_part)
plt.show()
plt.plot(imaginary_part)
plt.show()

# plot partial signal

partial_signal_FFT = np.fft.fft(partial_signal)
real_part = np.real(partial_signal_FFT)
imaginary_part = np.imag(partial_signal_FFT)

plt.plot(real_part)
plt.show()
plt.plot(imaginary_part)
plt.show()