import librosa
import numpy as np
import matplotlib.pyplot as plt

def load_audio_file(file_path, sample_rate = 16000):
    signal, sr = librosa.load(file_path, sr=sample_rate)
    return signal, sr

def compute_fft(signal, sample_rate = 16000):
    fft_result= np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1.0/sample_rate)
    frequencies = frequencies[:int(len(frequencies)/2)] 
    fft_result = fft_result[:int(len(fft_result)/2)]
    return frequencies, fft_result

def compute_power_spectrum(signal, sample_rate = 16000):
    frequencies, fft_result = compute_fft(signal, sample_rate)
    power_spectrum = np.abs(fft_result)**2 / len(signal)
    return frequencies, power_spectrum

def plot_power_spectrum(signal, sample_rate = 16000):
    frequencies, power_spectrum = compute_power_spectrum(signal, sample_rate)
    plt.ion()
    plt.clf()
    plt.plot(frequencies, power_spectrum)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.grid(alpha=0.3)
    plt.show()

def frequency_band_to_db(freq_lower_bound, freq_upper_band, frequencies, power_spectrum,
    baseline_power = 10**-12):
    lower_index = np.where(frequencies >= freq_lower_bound)[0][0]
    upper_index = np.where(frequencies <= freq_upper_band)[0][-1]
    power = np.sum(power_spectrum[lower_index:upper_index])
    return 10 * np.log10(power / baseline_power)
