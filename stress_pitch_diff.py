import frequency_band
import json
import librosa
import numpy as np
import matplotlib.pyplot as plt


def handle_vowel(word, vowel):
    '''compute the power in four frequency bands and convert to decibels
    for a specific vowel in a word.
    word        word class object from word module
    phoneme     phoneme class object from word module
    '''
    signal, sr = frequency_band.load_audio_file(word.audio_filename, 
        start=vowel.start_time, end=vowel.end_time)
    pitch = librosa.yin(signal, fmin = 65, fmax = 600, sr=sr)
    pitch = round(np.mean(pitch),3)
    return pitch

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
        pitch = handle_vowel(word, p)
        if pitch: line.append(pitch)
        else: continue
        output.append(line)
    return output

def mald_header():
    '''header for the vowel spectral balance dataset.
    dataset is created with handle_mald_words function
    '''
    h = ['word', 'ipa', 'audio_filename', 'phoneme', 'stressed','phoneme_index']
    h+= ['start_time', 'end_time', 'pitch']
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
        with open('../MALD/mald_pitch.json','w') as f:
            json.dump(output, f)
    return output

def load_pitch_json():
    d = json.load(open('../MALD/mald_pitch.json'))
    return d

def combine_multisyllable_word_lines(d = None):
    if not d: d = load_pitch_json()
    output = {}
    for line in d[1:]:
        word = line[0]
        if word not in output.keys(): output[word] = [line]
        else: output[word].append(line)
    # select only words with more than 1 syllable
    output = {word:line for word,line in output.items() if len(line) > 1}
    return output

def _find_stressed_unstressed(lines, one_word = False):
    stressed = [line[-1] for line in lines if line[4]]
    unstressed = [line[-1] for line in lines if not line[4]]
    if one_word:
        if len(stressed) != 1: return None, None
        stressed = stressed[0]
    return stressed, unstressed

def plot_hist_all_vowels(d = None, new_figure = True, ylim = None,
        add_legend = True, add_left = True, minimal_frame = False):
    if not d: d = load_pitch_json()
    plt.ion()
    if new_figure: plt.figure()
    ax = plt.gca()
    if minimal_frame:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    stressed, unstressed = _find_stressed_unstressed(d[1:])
    plt.ylim(ylim)
    plt.xlim(50, 350)
    plt.hist(stressed, bins = 50, alpha=0.7, color = 'black', 
        label = 'stressed')
    plt.hist(unstressed, bins = 50, alpha=0.7, color = 'orange', 
        label = 'unstressed')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xlabel('Pitch (Hz)')
    if add_left: plt.ylabel('Counts')
    else:
        ax.spines['left'].set_visible(False)
        ax.tick_params(left = False)
        ax.set_yticklabels([])
    plt.show()

def compute_pitch_difference(d = None, multiple = False):
    if not d: d = load_pitch_json()
    d = combine_multisyllable_word_lines(d)
    output = []
    for word, lines in d.items():
        stressed, unstressed = _find_stressed_unstressed(lines, one_word = True)
        if not stressed or not unstressed: continue
        if not multiple:
            pitch_diff = stressed - np.mean([x for x in unstressed])
            output.append(pitch_diff)
        else:
            pitch_diff = [stressed - x for x in unstressed]
            output.extend(pitch_diff)
    return output

def plot_pitch_difference(d = None, multiple = False):
    pitch_diff = compute_pitch_difference(d, multiple)
    plt.ion()
    plt.figure()
    plt.hist(pitch_diff, bins = 50, color = 'black')
    plt.grid(alpha=0.3)
    plt.xlabel('Pitch (Hz) difference')
    plt.ylabel('Counts')
    plt.show()
