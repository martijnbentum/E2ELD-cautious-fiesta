import descriptive_statistics as ds
from matplotlib import pyplot as plt
import numpy as np
import word

def compute_praat_intensity(signal):
    '''
    compute the intensity of a signal using praat's intensity algorithm
    '''
    baseline = 4 * 10 ** -10
    power = np.mean(signal ** 2)
    return 10 * np.log10(power / baseline)

def get_syllables(w = None):
    '''
    get all syllables from the mald dataset words
    '''
    if w is None: w = word.Word()
    syllables = ds.collect_syllables_ld(w, language='english')
    return syllables

def get_intensity_from_syllables(syllables = None, w = None):
    ''' get the duration of all stressed and unstressed syllables in 
    the mald dataset
    '''
    if not syllables: syllables = get_syllables(w)
    intensities = {'stress':[], 'no stress':[]} 
    for syllable in syllables:
        intensity = compute_praat_intensity(syllable.signal)
        if intensity == float('-inf'): continue
        if syllable.stressed: intensities['stress'].append(intensity)
        else: intensities['no stress'].append(intensity)
    return intensities 

def get_intensity_from_vowels(syllables = None, w = None):
    if not syllables: syllables = get_syllables(w)
    intensities= {'stress':[], 'no stress':[]} 
    for syllable in syllables:
        try: syllable.vowel
        except: continue
        intensity = compute_praat_intensity(syllable.vowel.signal)
        if intensity == float('-inf'): continue
        if syllable.stressed: 
            intensities['stress'].append(intensity)
        else: 
            intensities['no stress'].append(intensity)
    return intensities

def plot_stress_no_stress_distributions(intensities = None,
        w = None, use_syllable = False, new_figure = True,
        ylim = None, add_legend = True, minimal_frame = False):
    if not intensities:
        if use_syllable:
            intensities = get_intensity_from_syllables(w = w)
        else:
            intensities = get_intensity_from_vowels(w = w)
    plt.ion()
    if new_figure: plt.figure()
    ax = plt.gca()
    if minimal_frame:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.xlim(57, 81)
    if ylim: plt.ylim(ylim)
    plt.hist(intensities['stress'], bins=50, color = 'black', alpha=1, 
        label='stress')
    plt.hist(intensities['no stress'], bins=50, color = 'orange', alpha=.7,
        label='no stress')
    if add_legend: plt.legend()
    plt.xlabel('Intensity (dB)')
    plt.ylabel('Counts')
    plt.grid(alpha=0.3)

def boxplot_stress_no_stress_distributions(intensities = None, 
        w = None, use_syllable = False):
    if not intensities:
        if use_syllable:
            intensities = get_intensity_from_syllables(w = w)
        else:
            intensities = get_intensity_from_vowels(w = w)
    plt.ion()
    plt.figure()
    ax = plt.gca()
    outlier_properties = dict(marker='.', markerfacecolor='red', 
        markersize=8, markeredgecolor = None,alpha=0.5)
    plt.boxplot([intensities['stress'], intensities['no stress']], 
        labels=['stress', 'no stress'], flierprops=outlier_properties) 
    plt.ylabel('Intensity (dB)')
    plt.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
