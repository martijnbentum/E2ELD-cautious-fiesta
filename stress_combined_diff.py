import general
import numpy as np
from progressbar import progressbar
import stress_intensity_diff as sid
import frequency_band

def get_syllables(w = None):
    return sid.get_syllables(w)

def get_accoustic_correlates(syllables = None, w = None):
    if not syllables: syllables = get_syllables(w)
    X, y = [], []
    error = []
    for i,syllable in enumerate(progressbar(syllables)):
        if not syllable.vowel: 
            error.append([syllable, i])
            continue
        ac = syllable.vowel.accoustic_correlates
        if np.inf in ac:
            error.append([syllable, i])
            continue
        y.append(syllable.vowel.stressed)
        X.append(syllable.vowel.accoustic_correlates)
    return X, y, error

def compute_mccs_with_ci(X,y, n = 100):
    mccs = {'combined': []}
    for i in progressbar(range(n)):
        clf, data, report = frequency_band.train_lda(X,y, random_state=i)
        mccs['combined'].append(report['mcc'])
    print('done',np.mean(mccs['combined']), np.std(mccs['combined']))
    general.dict_to_json(mccs, '../mccs_combined_ac_lda_clf.json')
    return mccs
