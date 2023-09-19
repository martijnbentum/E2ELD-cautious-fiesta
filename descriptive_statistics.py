import celex
import word

def collect_syllables_ld(w = None, language = 'dutch'):
    if not w: 
        w = word.Words()
    words = [x for x in w.words if x.language == 'dutch' and x.is_word]
    syllables = []
    for x in words:
        syllables.extend(x.syllables)
    return syllables


def collect_syllables_celex(c = None, language = 'dutch'):
    if not c: c = celex.Celex('dutch') 
    syllables = []
    for x in c.words:
        for syllable in x.ipa_syllables:
            syllable = ' '.join(syllable)
            syllables.append(syllable)
    return syllables
    
def count_syllables(syllables):
    return Counter(syllables)

def baldey_syllable_dict(syllables = None, w = None):
    if not syllables: syllables = collect_syllables_ld(w, language = 'dutch')
    d = {}
    for syllable in syllables:
        if syllable.ipa not in d.keys(): d[syllable.ipa] = []
        d[syllable.ipa].append( syllable )
    return sort_dict_on_number_of_entries(d)

def stress_variability(syllable_dict, minimal_count = 10, perc_delta = .2):
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

def sort_dict_on_number_of_entries(d):
    d =dict(sorted(d.items(), key = lambda item:len(item[1]),reverse = True))
    return d

    
