import json
import librosa
import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import word

def load_audio_file(file_path, sample_rate = 16000, start = 0.0, end = None):
    '''load an audio file and return the signal and sample rate'''
    if end:
        duration = end - start
    else: duration = None
    signal, sr = librosa.load(file_path, sr=sample_rate, offset=start, 
        duration=duration)
    return signal, sr

def compute_fft(signal, sample_rate = 16000):
    '''compute the fast fourier transform of a signal
    returns only the positive frequencies
    frequencies         a list of frequencies corresponding to the fft_result
    fft_result          a list of complex numbers -> fourier decomposition
                        of the signal
    '''
        
    fft_result= np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1.0/sample_rate)
    frequencies = frequencies[:int(len(frequencies)/2)] 
    fft_result = fft_result[:int(len(fft_result)/2)]
    return frequencies, fft_result

def compute_power_spectrum(signal, sample_rate = 16000):
    '''compute the power spectrum of a signal
    frequencies         a list of frequencies corresponding to the fft_result
    power_spectrum      a list of real numbers -> power of the signal at each
                        frequency in frequencies
    '''
    frequencies, fft_result = compute_fft(signal, sample_rate)
    power_spectrum = np.abs(fft_result)**2 / len(signal)
    return frequencies, power_spectrum

def plot_power_spectrum(signal, sample_rate = 16000):
    '''plot the power spectrum of a signal'''
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
    '''compute the power in a frequency band and convert to decibels
    '''
    lower_index = np.where(frequencies >= freq_lower_bound)[0][0]
    upper_index = np.where(frequencies <= freq_upper_band)[0][-1]
    power = np.sum(power_spectrum[lower_index:upper_index])
    return round(10 * np.log10(power / baseline_power), 2)

def get_four_fb_to_db(frequencies, power_spectrum):
    '''compute the power in four frequency bands and convert to decibels
    the frequency bands are based on the article Sluijter & van Heuven (1994)
    to predict stress in vowels.
    '''
    fb1 = frequency_band_to_db(0, 500, frequencies, power_spectrum)
    fb2 = frequency_band_to_db(500, 1000, frequencies, power_spectrum)
    fb3 = frequency_band_to_db(1000, 2000, frequencies, power_spectrum)
    fb4 = frequency_band_to_db(2000, 4000, frequencies, power_spectrum)
    return fb1, fb2, fb3, fb4

def handle_vowel(word, vowel):
    '''compute the power in four frequency bands and convert to decibels
    for a specific vowel in a word.
    word        word class object from word module
    phoneme     phoneme class object from word module
    '''
    signal, sr = load_audio_file(word.audio_filename, start=vowel.start_time, 
        end=vowel.end_time)
    frequencies, power_spectrum = compute_power_spectrum(signal)
    output = get_four_fb_to_db(frequencies, power_spectrum)
    if sum([x < 0 for x in output]) > 0: return None
    return output

def handle_word(word):
    '''compute the power in four frequency bands and convert to decibels
    for every vowel in a word.
    word        word class object from word module
    '''
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
    '''header for the vowel spectral balance dataset.
    dataset is created with handle_mald_words function
    '''
    h = ['word', 'ipa', 'audio_filename', 'phoneme', 'stressed','phoneme_index']
    h+= ['start_time', 'end_time', 'fb1', 'fb2', 'fb3', 'fb4']
    return h

def handle_mald_words(w = None, save = False):
    '''create a dataset of vowel spectral balance for the mald dataset
    '''
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
    '''convert vowel spectral balance dataset to numpy arrays
    for LDA training.
    '''
    d = json.load(open('../MALD/mald_spectral_tilt.json'))[1:]
    X = np.zeros((len(d), 4))
    y = np.zeros((len(d), 1))
    for index, line in enumerate(d):
        X[index] = line[8:]
        y[index] = line[4]
    return X, y
        
def train_lda(X, y, test_size = 0.33, report = True):
    '''train an LDA based on the vowel spectral balance datase 
    use make_dataset function to create the dataset (X, y)
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        X,y, test_size = test_size, random_state=42)
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_train, y_train)
    if report:
        y_pred = clf.predict(X_test)
        print(classification_report(y_test, y_pred))
    data = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train}
    return clf, data
        
def plot_lda(X, y):
    ''' fit an LDA based on data (X) and labels (y) and plot the results
    '''
    plt.ion()
    plt.clf()
    clf, _ = train_lda(X, y, report = False)
    tf = clf.transform(X)
    color = ['blue', 'red']
    labels = ['no stress', 'stress']
    for color, i, label in zip(color, [0,1], labels):
        if i == 0: marker = 'o'
        else: marker = 'x'
        n = len(tf[y==i])
        plt.scatter(tf[y==i], np.random.random(n), alpha=.05, color=color,
            label=label, marker = marker)
    legend = plt.legend()
    for lh in legend.legendHandles:
        lh.set_alpha(1)
    plt.show()

def plot_lda_hist(X, y):
    plt.ion()
    plt.figure()
    clf, _ = train_lda(X, y, report = False)
    tf = clf.transform(X)
    plt.hist(tf[y==0], bins = 50, alpha=0.7, color = 'blue', 
        label = 'unstressed')
    plt.hist(tf[y==1], bins = 50, alpha=0.7, color = 'red', 
        label = 'stressed')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xlabel('Linear Discriminant score')
    plt.ylabel('Counts')
    plt.show()

def collect_fb_stressed_unstressed():
    '''collect the fb values for stressed and unstressed vowels
    '''
    d = json.load(open('../MALD/mald_spectral_tilt.json'))[1:]
    stressed = []
    unstressed = []
    for line in d:
        if line[4]: stressed.append(line[8:])
        else: unstressed.append(line[8:])
    return np.array(stressed), np.array(unstressed)

def plot_fb_stressed_unstressed():
    stressed, unstressed = collect_fb_stressed_unstressed()
    plt.ion()
    plt.figure()
    plt.plot(np.mean(stressed, 0))
    plt.plot(np.mean(unstressed, 0))
    plt.xticks([0,1,2,3],
        labels=['0 - 500','500 - 1000','1000 - 2000','2000 - 4000'])
    plt.ylabel('Intensity in dB')
    plt.xlabel('Frequency band')
    plt.legend(['stressed','unstressed'])
    plt.grid(alpha=.3)



