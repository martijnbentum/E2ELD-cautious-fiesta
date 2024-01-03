import json
import librosa
import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import word

def load_audio_file(file_path, sample_rate = 16000, start = 0.0, end = None):
    if end:
        duration = end - start
    else: duration = None
    signal, sr = librosa.load(file_path, sr=sample_rate, offset=start, 
        duration=duration)
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

def frequency_band_to_db(freq_lower_bound, freq_upper_band, frequencies, 
    power_spectrum, baseline_power = 10**-6):
    lower_index = np.where(frequencies >= freq_lower_bound)[0][0]
    upper_index = np.where(frequencies <= freq_upper_band)[0][-1]
    power = np.sum(power_spectrum[lower_index:upper_index])
    return round(10 * np.log10(power / baseline_power), 2)

def get_four_fb_to_db(frequencies, power_spectrum):
    fb1 = frequency_band_to_db(0, 500, frequencies, power_spectrum)
    fb2 = frequency_band_to_db(500, 1000, frequencies, power_spectrum)
    fb3 = frequency_band_to_db(1000, 2000, frequencies, power_spectrum)
    fb4 = frequency_band_to_db(2000, 4000, frequencies, power_spectrum)
    return fb1, fb2, fb3, fb4

def handle_vowel(word, vowel):
    signal, sr = load_audio_file(word.audio_filename, start=vowel.start_time, 
        end=vowel.end_time)
    frequencies, power_spectrum = compute_power_spectrum(signal)
    output = get_four_fb_to_db(frequencies, power_spectrum)
    if sum([x < 0 for x in output]) > 0: return None
    return output

def handle_word(word):
    if not word.table.phonemes: return None
    output = []
    for p in word.table.phonemes:
        line = [word.word, word.ipa, word.audio_filename, p.ipa, p.stressed]
        line.extend([p.phoneme_index,p.start_time, p.end_time])
        if p.phoneme_type != 'vowel': continue
        fbs = handle_vowel(word, p)
        if fbs: line.extend(fbs)
        else: continue
        output.append(line)
    return output

def mald_header():
    h = ['word', 'ipa', 'audio_filename', 'phoneme', 'stressed','phoneme_index']
    h+= ['start_time', 'end_time', 'fb1', 'fb2', 'fb3', 'fb4']
    return h

def handle_mald_words(w = None, save = False):
    if not w: w = word.Words()
    output = []
    for word in w.words:
        try: print(word)
        except: 
            print(word.word,'errror, skipping this word')
            continue
        if not word.is_word: continue
        if word.dataset != 'mald': continue
        o = handle_word(word)
        if o: output.extend(o)
    output.insert(0, mald_header())
    if save:
        with open('../MALD/mald_spectral_tilt.json','w') as f:
            json.dump(output, f)
    return output
    
def make_dataset():
    d = json.load(open('../MALD/mald_spectral_tilt.json'))[1:]
    X = np.zeros((len(d), 4))
    y = np.zeros((len(d), 1))
    for index, line in enumerate(d):
        X[index] = line[8:]
        y[index] = line[4]
    return X, y
        
def train_lda(X, y, test_size = 0.33, report = True):
    X_train, X_test, y_train, y_test = train_test_split(
        X,y, test_size = test_size, random_state=42)
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_train, y_train)
    if report:
        y_pred = clf.predict(X_test)
        print(classification_report(y_test, y_pred))
    data = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train}
    return clf, data
        
