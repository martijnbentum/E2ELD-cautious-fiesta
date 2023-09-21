import json
import locations
import os
import prosodic
import word as w


def analyze(word, save = True, strict = True):
    t = prosodic.Text(word)
    d = {}
    d['word'] = word
    d['syllables'] = [handle_syllable(s) for s in t.syllables()]
    if save: 
        if strict and not d['syllables']: 
            print('not saving because no syllables found')
            return d
        else:save_json(d)
    return d

def handle_syllable(syllable):
    d = {}
    d['ipa'] = syllable.str_ipa()
    d['arpabet'] = syllable.str_cmu()
    d['stressed'] = syllable.stressed
    d['stress_type'] = syllable.stress
    return d

def save_json(d):
    filename = locations.mald_prosodic_syllables_directory + d['word'] + '.json'
    with open(filename, 'w') as fout:
        json.dump(d,fout)

def load_json(word):
    filename = locations.mald_prosodic_syllables_directory + word + '.json'
    with open(filename) as fin:
        d = json.load(fin)
    return d
    
    
def dict_to_n_phonemes(d):
    n = 0
    for s in d['syllables']:
        n += len(s['arpabet'].split(' '))
    return n
