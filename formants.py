import locations
import matplotlib.pyplot as plt
import numpy as np
import os
from progressbar import progressbar

vowels = ['ɪ', 'ɛ', 'æ', 'ɑ', 'ʌ', 'ɔ', 'ʊ', 'u', 'i', 'ɝ']

def select_mald_words(w = None):
    if w is None:
        import word
        w = word.Words()
    words = [x for x in w.words if x.language == 'english' and x.is_word]
    words = [x for x in words if not x.syllable_error]
    return words

def make_vowel_f1_f2_stress_dict(w = None, use_mean_per_vowel = True):
    words = select_mald_words(w = w)
    d = {vowel:{'stressed':{'f1':[],'f2':[]}, 
            'unstressed':{'f1':[], 'f2': []}} for vowel in vowels}
    for word in progressbar(words):
        for phoneme in word.table.phonemes:
            if phoneme.ipa not in vowels: continue
            stress_key = 'stressed' if phoneme.stressed else 'unstressed'
            if use_mean_per_vowel:
                f1, f2 = phoneme.mean_f1_f2
                d[phoneme.ipa][stress_key]['f1'].append(f1)
                d[phoneme.ipa][stress_key]['f2'].append(f2)
            else:
                f1, f2 = phoneme.f1_f2
                d[phoneme.ipa][stress_key]['f1'].extend(f1)
                d[phoneme.ipa][stress_key]['f2'].extend(f2)
    return d

def vowel_global_f1_f2(w = None, sd = None):
    if not sd: sd = make_vowel_f1_f2_stress_dict(w)
    d = {vowel:{'f1':[],'f2':[]} for vowel in vowels}
    for vowel in progressbar(sd.keys()):
        for stress in sd[vowel].keys():
            d[vowel]['f1'].extend(sd[vowel][stress]['f1'])
            d[vowel]['f2'].extend(sd[vowel][stress]['f2'])
    return d

def global_f1_f2(w = None, sd = None, gd = None):
    if not gd: gd = vowel_global_f1_f2(w=w, sd=sd)
    f1, f2 = [], []
    for vowel in gd.keys():
        f1.append(np.mean(gd[vowel]['f1']))
        f2.append(np.mean(gd[vowel]['f2']))
    return f1, f2
            
def global_mean_f1_f2(w = None, sd = None, gd = None):
    if not gd: gd = vowel_global_f1_f2(w=w, sd=w)
    f1 = np.mean([np.mean(gd[vowel]['f1']) for vowel in gd.keys()])
    f2 = np.mean([np.mean(gd[vowel]['f2']) for vowel in gd.keys()])
    return f1, f2

def make_stress_no_stress_dict(w = None, sd = None):
    if not sd: sd = make_vowel_f1_f2_stress_dict(w=w)
    stress = {}
    for vowel, stress_dict in sd.items():
        for stress_key, f1f2 in stress_dict.items():
            if stress_key not in stress: stress[stress_key] = {'f1':[],'f2':[]} 
            for fk, values in f1f2.items():
                stress[stress_key][fk].extend(stress_dict[stress_key][fk])
    return stress
        

def compute_distance_to_global_mean(w = None, sd = None, gd = None, 
        stress = None):
    if not stress:stress = make_stress_no_stress_dict(w=w, sd=sd)
    global_f1, global_f2 = global_mean_f1_f2(w=w, sd=sd, gd=gd)
    for stress_key, f1f2 in stress.items():
        if not 'distance' in f1f2.keys():f1f2['distance'] = []
        for f1, f2 in zip(f1f2['f1'], f1f2['f2']):
            distance = np.sqrt((global_f1 - f1)**2 + (global_f2 - f2)**2)
            f1f2['distance'].append(distance)
    return stress
            

def plot_stress_no_stress(stress_distance = None, w = None, sd = None, 
        gd = None, new_figure = True,add_legend = True, add_left = True,
        minimal_frame = False, ylim = None):
    if not stress_distance: 
        stress_distance = compute_distance_to_global_mean(w=w, sd=sd, gd=gd)
    if new_figure: plt.figure()
    ax = plt.gca()
    if minimal_frame:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.ion()
    plt.xlim(0,850)
    if ylim: plt.ylim(ylim)
    plt.hist(stress_distance['stressed']['distance'], color = 'black',bins = 50,
        label = 'stress')
    plt.hist(stress_distance['unstressed']['distance'], color = 'orange', 
        bins = 50, alpha = 0.7, label = 'no stress')
    plt.grid(alpha = 0.3)
    plt.xlabel('Formants (Hz)')
    if add_legend: plt.legend()
    if add_left: plt.ylabel('Counts')
    else:
        ax.spines['left'].set_visible(False)
        ax.tick_params(left = False)
        ax.set_yticklabels([])
        
    plt.show()
    
        

def plot_formants(w = None, sd = None, gd = None):
    if not sd: sd = make_vowel_f1_f2_stress_dict(w)
    if not gd: gd = vowel_global_f1_f2(w, sd)
    f1, f2 = global_f1_f2(w, sd, gd)
    plt.figure()
    plt.ion()
    plt.xlim(2100, 1050)
    plt.ylim(650, 350)
    plt.scatter(f2, f1,color = 'lightgrey', marker= '.', label = 'vowel mean')
    for vowel in gd.keys():
        plt.text(np.mean(gd[vowel]['f2'])+7.5, np.mean(gd[vowel]['f1'])-4, vowel,
            color = 'lightgrey', fontsize = 16)
        for stress in ['stressed', 'unstressed']:
            stress_label = 'stress' if stress == 'stressed' else 'no stress'
            if vowel == 'ɪ': label =stress_label
            else: label = None
            color = 'black' if stress == 'stressed' else 'orange'
            sf1 = np.mean(sd[vowel][stress]['f1'])
            sf2 = np.mean(sd[vowel][stress]['f2'])
            plt.scatter(sf2, sf1, marker = '.',color = color, label = label) 
            plt.text(sf2+7.5, sf1-4, vowel, color = color, fontsize = 16)
    plt.scatter(np.mean(f2), np.mean(f1), marker = 'x', color = 'red', 
        label = 'global mean')
    plt.grid(alpha = 0.3)
    plt.legend()
    plt.xlabel('F2')
    plt.ylabel('F1')
    plt.show()

class Formants:
    '''class to handle formant values for a word
    formant values are stored in a table file
    the formant values are computed with Praat
    '''
    def __init__(self, word):
        self.word = word
        self.table, self.header = load_formants(word)
        self._make_formant_lines()

    def _make_formant_lines(self):
        self.formant_lines = [Formant_line(x) for x in self.table]

    def interval(self, start, end):
        lines = self.formant_lines
        lines = [x for x in lines if x.time >= start and x.time <= end]
        return lines

    def interval_mean_f1_f2(self, start, end):
        lines = self.interval(start, end)
        f1 = round(sum([x.f1 for x in lines]) / len(lines),3)
        f2 = round(sum([x.f2 for x in lines]) / len(lines),3)
        return f1, f2

    def mean_f1_f2(self, item):
        '''return mean f1 and f2 for item, typically a phoneme object
        phoneme object is defined in word.py
        '''
        start, end = item.start_time, item.end_time
        return self.interval_mean_f1_f2(start, end)

    def f1_f2(self, item):
        '''return all f1 and f2 values for item, typically a phoneme object
        phoneme object is defined in word.py
        '''
        start, end = item.start_time, item.end_time
        lines = self.interval(start, end)
        f1 = [x.f1 for x in lines]
        f2 = [x.f2 for x in lines]
        return f1, f2

class Formant_line:
    '''line from formant table with time and formant values'''
    def __init__(self, line):
        self.line = line
        self.time = float(line[0])
        self.nformants = int(line[1])
        self.f1 = float(line[2])
        self.f2 = float(line[4])

    def __repr__(self):
        return 'Time: {}, F1: {}, F2: {})'.format(self.time, self.f1, self.f2)




def load_formants(word):
    '''load table file with formant values for word
    word is a word object defined in word.py
    '''
    filename = word_to_formant_filename(word)
    with open(filename, 'r') as f:
        temp= [x.split('\t') for x in f.read().split('\n') if x]
    header, table = temp[0], temp[1:]
    return table, header

# make formant table files for all words in mald dataset

def absolute_path_dir(path):
    home = os.getenv('HOME') + '/Documents/indeep/LD/'
    absolute = path
    absolute = absolute.replace('../', home)
    return absolute

def word_to_formant_filename(word):
    formant_file = absolute_path_dir(locations.mald_formant_dir)
    formant_file += word.audio_filename.split('/')[-1].split('.')[0] + '.Table'
    return formant_file
    

def word_praat_cmd(word):
    formant_file = word_to_formant_filename(word)
    audio_filename = absolute_path_dir(word.audio_filename) 
    name = word.word.upper()
    cmd = []
    cmd.append('Read from file: "{}"'.format(audio_filename))
    cmd.append('To Formant (burg): 0, 5, 5500, 0.025, 50')
    cmd.append('Down to Table: "no", "yes", 6, "no", 3, "yes", 3, "yes"')
    cmd.append('Save as tab-separated file: "{}"'.format(formant_file))
    cmd.append('selectObject: "Sound {}"'.format(name))
    cmd.append('plusObject: "Formant {}"'.format(name))
    cmd.append('plusObject: "Table {}"'.format(name))
    cmd.append('Remove')
    return '\n'.join(cmd)

def make_praat_script_for_all_mald_words(w = None):
    script = []
    words = select_mald_words(w)
    for word in words:
        script.append(word_praat_cmd(word))
    filename = absolute_path_dir(locations.mald_formant_dir) 
    filename += 'formant_script.praat'
    with open(filename, 'w') as f:
        f.write('\n'.join(script))
    return '\n'.join(script)
    
