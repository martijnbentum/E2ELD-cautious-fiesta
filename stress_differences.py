import descriptive_statistics as ds
from matplotlib import pyplot as plt
import numpy as np
import word

def get_syllables(w = None):
    '''
    get all syllables from the mald dataset words
    '''
    if w is None: w = word.Word()
    syllables = ds.collect_syllables_ld(w, lang='english')
    return syllables

def get_durations_from_syllables(syllables = None, w = None):
    ''' get the duration of all stressed and unstressed syllables in 
    the mald dataset
    '''
    if not syllables: syllables = get_syllables(w)
    durations = {'stress':[], 'no stress':[]} 
    for syllable in syllables:
        if syllable.stressed: durations['stress'].append(syllable.duration)
        else: durations['no stress'].append(syllable.duration)
    return durations

def get_syllables_from_multi_syllable_words(syllables = None, w = None):
    '''select all syllables from multi syllable words.
    only one syllable per word is selected
    assumes the syllable is the Syllable class defined in word.py 
    '''
    if not syllables: syllables = get_syllables(w)
    words = []
    output = []
    for syllable in syllables:
        if len(syllable.word.syllables) > 1 and syllable.word not in words: 
            output.append(syllable)
            words.append(syllable.word)
    return output

def syllable_to_vowel(syllable):
    '''select the vowel from all phonemes in a syllable
    assumes the syllable is the Syllable class defined in word.py 
    '''
    for phoneme in syllable.phonemes:
        if phoneme.phoneme_type == 'vowel': return phoneme
   
def word_stress_duration_difference(word, multiple = False):
    '''computes the difference in duration between stressed and unstressed
    vowels in a word
    difference = stressed vowel duration - mean(unstressed vowels duration)
    if the value is positive the stressed vowel is longer than the unstressed
    vowels
    returns a dict with information
    '''
    no_stress_duration_total = []
    stressed_duration = 0
    for syllable in word.syllables:
        vowel = syllable_to_vowel(syllable)
        if not vowel: continue
        if vowel.stressed:
            stressed_duration = vowel.duration
        else:
            no_stress_duration_total.append( vowel.duration )
    no_stress_duration = np.mean(no_stress_duration_total)
    zero_duration = stressed_duration == 0 or no_stress_duration == 0
    diff = stressed_duration - no_stress_duration
    line = {'word': word, 'stressed duration': stressed_duration, 
        'no stress duration': no_stress_duration, 'difference': diff,
        'no stress duration total': no_stress_duration_total,
        'zero duration': zero_duration}
    if multiple:
        import copy
        lines = []
        for no_stress_duration in no_stress_duration_total:
            if no_stress_duration == 0: continue
            if stressed_duration == 0: continue
            line = copy.copy(line)
            line['no stress duration'] = no_stress_duration
            line['difference'] = stressed_duration - no_stress_duration
            lines.append(line)
        return lines
    return line

def mald_word_stress_duration_difference(w = None, multiple = False):
    '''computes the difference in duration between stressed and unstressed
    vowels in a word for all words in the mald dataset
    '''
    if w is None: w = word.Word()
    output = []
    for word in w.words:
        if word.dataset != 'mald': continue
        if not word.is_word: continue
        if not hasattr(word, 'syllables'): continue
        if len(word.syllables) < 2: continue
        o = word_stress_duration_difference(word, multiple = multiple)
        if multiple: 
            if o: output.extend(o)
            continue
        if o['zero duration']: continue
        if len(o['no stress duration total']) == 0: continue
        output.append(o)
    return output

def plot_distribution_of_stress_duration_differences(w = None, multiple = False):
    '''plot the distribution of stress duration differences
    '''
    data = mald_word_stress_duration_difference(w, multiple = multiple)
    differences = [x['difference'] for x in data]
    plt.ion()
    plt.figure()
    plt.hist(differences, bins=50, color = 'black')
    plt.grid(alpha=0.3)
    plt.xlabel('Duration in seconds')
    plt.ylabel('Counts')
