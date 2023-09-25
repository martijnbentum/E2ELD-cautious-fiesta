import celex
import word
from collections import Counter

def collect_syllables_ld(w = None, language = 'dutch'):
    if not w: 
        w = word.Words()
    words = [x for x in w.words if x.language == language and x.is_word]
    words = [x for x in words if not x.syllable_error]
    syllables = []
    for x in words:
        syllables.extend(x.syllables)
    return syllables


def collect_syllables_celex(c = None, language = 'dutch'):
    if not c: c = celex.Celex(language) 
    syllables = []
    for x in c.words:
        for syllable in x.ipa_syllables:
            syllable = ' '.join(syllable)
            syllables.append(syllable)
    return syllables
    
def count_syllables(syllables):
    return Counter(syllables)

def _syllable_dict(syllables):
    d = {}
    for syllable in syllables:
        if syllable.ipa not in d.keys(): d[syllable.ipa] = []
        d[syllable.ipa].append( syllable )
    return sort_dict_on_number_of_entries(d)

def baldey_syllable_dict(syllables = None, w = None):
    if not syllables: syllables = collect_syllables_ld(w, language = 'dutch')
    return _syllable_dict(syllables)

def _stress_variability(syllable_dict, minimal_count, perc_delta):
    d = {}
    variable = {}
    for ipa, syllables in syllable_dict.items():
        if len(syllables) == 1: continue
        stressed = len([x for x in syllables if x.stressed]) 
        unstressed = len(syllables) - stressed
        if stressed == 0 or unstressed == 0: v = False
        else: v = True
        d[ipa] = stressed, unstressed
        perc_stressed = round(stressed / len(syllables),2)
        if v:
            if len(syllables) < minimal_count: continue
            if perc_stressed < (.5-perc_delta):continue 
            if perc_stressed > (.5 + perc_delta):continue
            variable[ipa] = {'stressed':stressed,'unstressed':unstressed,
                'syllables':syllables,'perc_stressed':perc_stressed}
    return d, variable

def stress_variability_baldey(syllable_dict = None, minimal_count = 10, 
        perc_delta = .2):
    if not syllable_dict: syllable_dict = baldey_syllable_dict()
    return _stress_variability(syllable_dict, minimal_count, perc_delta)

def sort_dict_on_number_of_entries(d):
    d =dict(sorted(d.items(), key = lambda item:len(item[1]),reverse = True))
    return d

def _hapax_syllables(d):
    keys = [k for k,syllables in d.items() if len(syllables) ==1]
    hapax= []
    for k in keys: 
        hapax.extend( d[k] )
    return hapax
        
def hapax_baldey_syllables(d= None):
    if not d: d = baldey_syllable_dict()
    return _hapax_syllables(d)

def _top_n_syllable_type_count(d, n = 20):
    keys = list(d.keys())
    for k in keys[:n]:
        stressed = str(len([x for x in d[k] if x.stressed]))
        unstressed = str(len([x for x in d[k] if not x.stressed]))
        word = d[k][0].word.word
        ipa = d[k][0].word.ipa
        m ='|'+k+'|'+ str(len(d[k]))+'|'+stressed+'|'+unstressed+'|'
        m += word+'|'+ipa+'|'
        print(m)
   
def top_n_syllable_count_baldey(d = None, n = 20):
    if not d: d = baldey_syllable_dict()
    _top_n_syllable_type_count(d,n)

# ------------------------------------------------------------------------------
# mald
    
def mald_syllable_dict(syllables = None, w = None):
    if not syllables: syllables = collect_syllables_ld(w, language = 'english')
    return _syllable_dict(syllables)

def hapax_mald_syllables(d = None):
    if not d: d = mald_syllable_dict()
    return _hapax_syllables(d)

def top_n_syllable_count_mald(d = None, n = 20):
    if not d: d = mald_syllable_dict()
    _top_n_syllable_type_count(d,n)

def stress_variability_mald(syllable_dict = None, minimal_count = 10,
        perc_delta = .2):
    if not syllable_dict: syllable_dict = mald_syllable_dict()
    return _stress_variability(syllable_dict, minimal_count, perc_delta)
    
