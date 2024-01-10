import librosa
import numpy as np
import frequency_band


def handle_vowel(word, vowel):
    '''compute the power in four frequency bands and convert to decibels
    for a specific vowel in a word.
    word        word class object from word module
    phoneme     phoneme class object from word module
    '''
    signal, sr = frequency_band.load_audio_file(word.audio_filename, 
        start=vowel.start_time, end=vowel.end_time)
    pitch = librosa.yin(signal, fmin = 65, fmax = 600, sr=sr)
    if not pitch: return None
    return round(np.mean(pitch),3)

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


