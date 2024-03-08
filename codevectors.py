'''module for working with codevectors
a codevector is a concatenation of two codebook vectors
a codevector is represented by a pair of indices
'''

import copy
import general
import glob
import json
import locations
from matplotlib import pyplot as plt
import numpy as np
import os
import phoneme_mapper
import pickle
import sox
import word


if os.path.isfile(locations.fn_mald_codevector_indices):
    with open(locations.fn_mald_codevector_indices) as f:
        fn = f.read().split('\n')
else:
    fn = glob.glob(locations.mald_codevector_indices + '*.npy')
    fn = [f for f in fn if 'codebook' not in f]


def load_codebook_indices(filename):
    '''load codebook indices from a numpy file
    the indices are based on a cgn audio file
    '''
    return np.load(filename)

def load_codebook(filename=locations.codebook_filename):
    '''load the codebook
    the correct codebook depends on the module used to compute the 
    codebook indices
    '''
    return np.load(filename)

class Frames:
    '''object to handle wav2vec2 linking frames to phoneme transcriptions
    each frame has codebook indices representing a codevector
    each frame can be linked to a phoneme via the transcription
    each frame has a start and end time
    the frames have a step of 20ms and a duration of 25ms
    '''
    def __init__(self, fn = fn, words = None):
        if not words: words = word.Words()
        self.words = words
        self.frames = []
        self.filenames = []
        for f in fn:
            self.add_file(f)
        self.frame_set = set(self.frames)

    def add_file(self, filename):
        if 'codebook' in filename: return
        if filename in self.filenames:
            print('already added', filename)
            return
        self.filenames.append(filename)
        codebook_indices = load_codebook_indices(filename)
        self._add_frames(codebook_indices, filename)

    def __repr__(self):
        m = 'nframes: '+str(len(self.frames)) 
        m += ' ' + str(len(set(self.frames)))
        return m

    def _add_frames(self, codebook_indices, filename):
        for index, ci in enumerate(codebook_indices):
            frame = Frame(index, ci, self, filename)
            self.frames.append(frame)

    def get_codevector(self, codebook_indices):
        i1, i2 = codebook_indices
        half = self.codebook.shape[1] // 2
        q1 = self.codebook[i1]
        q2 = self.codebook[i2]
        return np.concatenate([q1, q2], axis=0)

    @property
    def codebook(self):
        return load_codebook()

class Frame:
    '''object to store information for a specific frame
    '''
    def __init__(self, index, codebook_indices, parent, filename):
        self.index = index
        self.codebook_indices = codebook_indices
        self.parent = parent
        self.filename = filename
        self.name = filename.split('/')[-1].split('.')[0]
        self.start, self.end = frame_index_to_times(index)
        self.i1, self.i2 = map(int,self.codebook_indices)
        self.key = (self.i1, self.i2)

    def __repr__(self):
        m = str(self.index) + ' ' + str(self.codebook_indices)
        m += ' ' + str(self.start) + ' ' + str(self.end)
        return m

    def __eq__(self, other):
        #check if codevector is identical
        if type(self) != type(other):return False
        return self.i1== other.i1 and self.i2 == other.i2

    def __hash__(self):
        return hash((self.i1, self.i2))

    @property
    def word(self):
        if hasattr(self,'_word'): return self._word
        self._word = self.parent.words.get_word(self.name.lower())
        if len(self._word) > 1: 
            for x in self._word:
                if x.dataset == 'mald': self._word = x
        else: self._word = self._word[0]
        return self._word

    @property
    def phoneme(self):
        '''the phoneme linked to the frame
        the selected phoneme is the one with the largest overlap
        with the frame start and end time
        '''
        if hasattr(self,'_phoneme') and self._phoneme: 
            return self._phoneme
        s1, e1 = self.start,self.end
        self._phoneme = None
        self._phoneme_duration = 0
        phonemes = _get_all_mald_phonemes(self.word)
        for phoneme in phonemes:
            s2, e2 = phoneme.start_time, phoneme.end_time
            if general.overlap(s1,e1,s2,e2):
                duration = general.overlap_duration(s1,e1,s2,e2)
                if self._phoneme and duration < self._phoneme_duration: 
                    continue
                self._phoneme = phoneme
                self._phoneme_duration = duration
        return self._phoneme

    @property
    def codevector(self):
        '''the codevector for the frame
        based on the indices
        '''
        return self.parent.get_codevector(self.codebook_indices)


def frame_index_to_times(index, step = 0.02, duration = 0.025):
    '''compute the start and end time for a frame
    '''
    start = index * step
    end = start + duration
    return round(start,3), round(end,3)
        
    
    
def make_frame_dict(frames):
    '''make a dictionary of frames
    the identifier for a frame is the pair of indices linking it to the 
    codebook
    '''
    d = {}
    for frame in frames:
        key = (frame.i1, frame.i2)
        if not key in d.keys(): d[key] = []
        d[key].append(frame)
    return d


def frames_to_phoneme_counter(frames, add_stress_info = False, 
    add_time_info = False):
    '''for frames from a single codevector type, count the phonemes 
    that are linked to it
    '''
    if add_stress_info and add_time_info:
        raise ValueError('cannot add stress and time info')
    d = {}
    for frame in frames:
        if not frame.phoneme: continue
        ipa = frame.phoneme.ipa
        if add_stress_info and ipa != 'silence':
            if frame.phoneme.stressed: ipa += '_stressed'
        if add_time_info and ipa != 'silence':
            ipa += '_' + frame_to_begin_middle_end_all(frame)
        if not ipa in d.keys(): d[ipa] = 0
        d[ipa] += 1
    return d


def dict_to_sorted_dict(d):
    '''sort a dict based on the values
    '''
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

def count_dict_to_probability_dict(d):
    '''convert a count dict to a probability dict
    '''
    od = copy.copy(d)
    total = sum(d.values())
    for key in d.keys():
        od[key] /= total
    return od

def frames_to_count_dict(frames, add_stress_info = False, 
    add_time_info = False, save = False):
    '''for frames from a single codevector type
    create a count dict for the phonemes linked to the frames
    optionally stor it as a json file
    '''
    if add_stress_info and add_time_info:
        raise ValueError('cannot add stress and time info')
    key = frames[0].key
    d = frames_to_phoneme_counter(frames, add_stress_info, add_time_info)
    d = dict_to_sorted_dict(d)
    if save:
        if add_stress_info:
            filename = locations.mald_codevector_phoneme_count_stress_info
        elif add_time_info:
            filename = locations.mald_codevector_phoneme_count_time_info
        else:
            filename = locations.mald_codevector_phoneme_count
        filename += '-'.join(map(str,key)) + '.json'
        json.dump(d, open(filename, 'w'))
    return d

    
def load_count_dict(filename):
    '''load a codevector phoneme count dict.'''
    d = json.load(open(filename))
    od ={}
    for key in d.keys():
        if key[0] == '!': continue
        if key == '[]': continue
        od[key] = d[key]
    return od


def load_all_count_dicts(add_stress_info = False, add_time_info = False):
    '''load all codevector phoneme count dicts.'''
    if add_stress_info and add_time_info:
        raise ValueError('cannot add stress and time info')
    if add_stress_info:
        path = locations.mald_codevector_phoneme_count_stress_info + '*.json'
    elif add_time_info:
        path = locations.mald_codevector_phoneme_count_time_info + '*.json'
    else:
        path = locations.mald_codevector_phoneme_count+ '*.json'
    filenames = glob.glob(path)
    to_name = codevector_json_filename_to_name
    return dict([[to_name(f), load_count_dict(f)] for f in filenames])

def _check_time_info(p):
    for x in p:
        if '_begin' in x or '_middle' in x or '_end' in x: return True
    return False

def _group_phonemes_by_bpc_time_info(p):
    ipa = phoneme_mapper.ipa_set
    output = []
    for phoneme in ipa:
        if phoneme + '_begin' in p: 
            output.append(phoneme + '_begin')
        if phoneme + '_middle' in p: 
            output.append(phoneme + '_middle')
        if phoneme + '_end' in p: 
            output.append(phoneme + '_end')
    for phoneme in p:
        if phoneme == 'silence': continue
        if phoneme not in output:
            phoneme = phoneme.split('_')[0]
            if phoneme + '_begin' in p and phoneme + '_begin' not in output: 
                output.append(phoneme + '_begin')
            if phoneme + '_middle' in p and phoneme + '_middle' not in output: 
                output.append(phoneme + '_middle')
            if phoneme + '_end' in p and phoneme + '_end' not in output: 
                output.append(phoneme + '_end')
    output.append('silence')
    return output

def group_phonemes_by_bpc(p):
    if _check_time_info(p): return _group_phonemes_by_bpc_time_info(p)
    ipa = phoneme_mapper.ipa_set
    output = []
    for phoneme in ipa:
        if phoneme in p: 
            output.append(phoneme)
            if phoneme + '_stressed' in p:
                output.append(phoneme + '_stressed')
    for phoneme in p:
        if phoneme == 'silence': continue
        if phoneme not in output:
            if '_stressed' in phoneme: 
                ns= phoneme.split('_stressed')[0]
                if ns in p: phoneme = ns
            output.append(phoneme)
            ps = phoneme + '_stressed'
            if ps in p and ps not in output:
                output.append(phoneme + '_stressed')
    output.append('silence')
    return output

def _get_all_phonemes(count_dicts, group_by_bpc = True):
    '''list all phonemes present in a set of codevector count dicts.'''
    d = count_dicts
    p = []
    for v in d.values():
        for k in v.keys():
            if k not in p: p.append(k)
    if group_by_bpc: p = group_phonemes_by_bpc(p)
    return p

def create_phoneme_codevector_counts(p, d):
    '''create dictionary that maps a phoneme to a codevector count dict.'''
    output_dict = {}
    for phoneme in p:
        output_dict[phoneme] = {}
        for codevector_filename, phoneme_count_dict in d.items():
            name = codevector_json_filename_to_name(codevector_filename)
            if phoneme not in phoneme_count_dict.keys(): phoneme_count = 0
            else: phoneme_count = phoneme_count_dict[phoneme]
            output_dict[phoneme][name] = phoneme_count
    return output_dict
        

def codevector_json_filename_to_name(filename):
    '''map the codevector phoneme count dict json filename to 
    the codevector name (the codebook indices: index1-index2)
    '''
    name = filename.split('/')[-1].split('.')[0]
    return name
    
def _get_vowel_indices(phonemes, stress_marker = '_stressed', vowels = None):
    if not vowels:
        vowels = phoneme_mapper.ipa_mald_vowels
    vowels_stressed = [x + stress_marker for x in vowels]
    indices = []
    for index, phoneme in enumerate(phonemes):
        if phoneme in vowels: indices.append(index)
        elif phoneme in vowels_stressed: indices.append(index)
    return indices
        
def create_matrix_phoneme_counts(p, d, only_vowels = False):
    '''create a matrix that with a phoneme per row and codevectors
    per column. The matrix values are the counts of the phoneme each 
    codevector column.
    '''
    if only_vowels:
        vowel_indices = _get_vowel_indices(p)
        p = [p[i] for i in vowel_indices]
    rows, columns = len(p), len(d)
    m = np.zeros((rows, columns))
    for i, phoneme in enumerate(p):
        for j, codevector_phoneme_counts in enumerate(d.values()):
            cpc = codevector_phoneme_counts
            if phoneme not in cpc.keys():
                m[i,j] = 0
                continue
            m[i,j] = cpc[phoneme]
    print(m.shape)
    if only_vowels:
        # bad_indices = np.where(np.isnan(np.sum(m, axis=0)))[0]
        zero_indices = np.where(np.sum(m, axis=0) == 0)[0]
        m = np.delete(m, zero_indices, axis=1)
        print(m.shape, zero_indices.shape)
    return m
            

def sort_probability_dict(d):
    '''sort a probability dict based on the values.
    '''
    o = (sorted(d.items(), key=lambda item: item[1], 
        reverse=True))
    return dict(o)


def compute_phoneme_pdf(d):
    '''computes a probability distribution over phonemes.
    '''
    output_d = {}
    p = _get_all_phonemes(d)
    m = create_matrix_phoneme_counts(p, d)
    all_count = np.sum(m)
    for i,phoneme in enumerate(p):
        output_d[phoneme] = np.sum(m[i]) / all_count
    return output_d

def compute_codevector_pdf(d):
    '''computes a probability distribution over codevectors.
    '''
    output_d = {}
    p = _get_all_phonemes(d)
    m = create_matrix_phoneme_counts(p, d)
    all_count = np.sum(m)
    for i,key in enumerate(d.keys()):
        # name = codevector_json_filename_to_name(key)
        output_d[key] = np.sum(m[:,i]) / all_count
    return output_d

def compute_phoneme_conditional_probability_matrix(d, only_vowels = False):
    '''compute the conditional probability matrix for P(phoneme | codevector).
    '''
    p = _get_all_phonemes(d)
    m = create_matrix_phoneme_counts(p, d, only_vowels)
    m = m / np.sum(m, axis=0)
    return m

def compute_codevector_conditional_probability_matrix(d, only_vowels = False):
    '''compute the conditional probability matrix for P(codevector | phoneme).
    '''
    p = _get_all_phonemes(d)
    m = create_matrix_phoneme_counts(p, d, only_vowels)
    m = m.transpose() / np.sum(m, axis=1)
    return m.transpose()

def _rename_stress_marker(p, new_marker = ' *',stress_marker = '_stressed'):
    output = []
    for x in p:
        if stress_marker in x:
            x = x.replace(stress_marker, new_marker)
            output.append(x)
        else: output.append(x)
    return output

def plot_phoneme_conditional_probability_matrix(d = None, 
    only_vowels = False, add_stress_info = False, add_time_info = False,
    set_stress_marker = ' *'):
    '''plot the conditional probability matrix for P(phoneme | codevector).
    '''
    if not d: d = load_all_count_dicts(add_stress_info, add_time_info)
    p = _get_all_phonemes(d)
    if only_vowels: 
        vowel_indices = _get_vowel_indices(p)
        p = [p[i] for i in vowel_indices]
    m = compute_phoneme_conditional_probability_matrix(d, only_vowels)
    row_index_max_value = np.argmax(m, axis=0)
    column_indices = np.argsort(row_index_max_value)
    m = m[:,column_indices]
    fig, ax = plt.subplots(figsize=(10,10))
    if add_stress_info: p = _rename_stress_marker(p, set_stress_marker)
    cax = ax.matshow(m, aspect = 150, cmap = 'binary')
    fig.colorbar(cax, fraction = .046, pad = .015)
    ax.yaxis.set_ticks(range(len(p)),p)
    xticks, xlabels = plt.xticks()
    plt.xticks(xticks[2:-2], xlabels[2:-2])
    plt.show()
    return m
        
def plot_codevector_conditional_probability_matrix(d = None):
    '''plot the conditional probability matrix for P(codevector | phoneme).
    '''
    if not d: d = load_all_count_dicts()
    p = _get_all_phonemes(d)
    m = compute_codevector_conditional_probability_matrix(d)
    row_index_max_value = np.argmax(m, axis=0)
    column_indices = np.argsort(row_index_max_value)
    m = m[:,column_indices]
    fig, ax = plt.subplots(figsize=(10,10))
    ax.matshow(m, aspect = 150,vmax=.05, cmap = 'binary')
    ax.yaxis.set_ticks(range(len(p)),p)
    plt.show()
    return m

def compute_phoneme_confusion_matrix(d = None, only_vowels = False):
    '''compute the confusion probability matrix for P(phoneme | phoneme).
    '''
    if not d: d = load_all_count_dicts()
    m = compute_phoneme_conditional_probability_matrix(d, only_vowels)
    mm = compute_codevector_conditional_probability_matrix(d, only_vowels)
    confusion_matrix = np.matmul(m,mm.transpose())
    return confusion_matrix

def _sampa_to_ipa(p):
    ipa_d= phonemes.Sampa().to_ipa_dict
    ipa_p = []
    for x in p:
        if x not in ipa_d.keys(): 
            if x == 'silence': x = 'sil'
            ipa_p.append(x)
        else: ipa_p.append(ipa_d[x])
    return ipa_p
    
def plot_phoneme_confusion_matrix(d = None, only_vowels = False):
    '''plot the confusion probability matrix for P(phoneme | phoneme).
    '''
    if not d: d = load_all_count_dicts()
    p = _get_all_phonemes(d)
    if only_vowels:
        vowel_indices = _get_vowel_indices(p)
        p = [p[i] for i in vowel_indices]
    m = compute_phoneme_confusion_matrix(d, only_vowels)
    fig, ax = plt.subplots(figsize=(10,10))
    ax.matshow(m, cmap = 'binary')
    ax.xaxis.set_ticks(range(len(p)),p)
    ax.yaxis.set_ticks(range(len(p)),p)
    plt.xticks(rotation=90)
    plt.show()
    return m
   

def _get_all_mald_phonemes(word):
    '''get all phonemes for a word.
    '''
    table = word.table
    duration = word.audio_info['duration']
    start_phoneme, end_phoneme = None, None
    if not table.phonemes: return []
    if table.phonemes[0].start_time > 0:
        start_phoneme = copy.copy(table.phonemes[0])
        start_phoneme.end_time = start_phoneme.start_time
        start_phoneme.start_time = 0
        start_phoneme.line = copy.copy(start_phoneme.line)
        start_phoneme.line[1] = 'silence'
    if table.phonemes[-1].end_time < word.duration:
        end_phoneme = copy.copy(table.phonemes[-1])
        end_phoneme.start_time = end_phoneme.end_time
        end_phoneme.end_time = duration
        end_phoneme.line = copy.copy(end_phoneme.line)
        end_phoneme.line[1] = 'silence'
    output = []
    if start_phoneme: output.append(start_phoneme)
    for x in word.table.phonemes:
        output.append(x)
    if end_phoneme: output.append(end_phoneme)
    return output
   

def _split_phoneme_time(phoneme):
    part_duration = phoneme.duration / 3
    begin = phoneme.start_time, phoneme.start_time + part_duration
    middle = begin[1], begin[1] + part_duration
    end = middle[1], phoneme.end_time
    return begin, middle, end


def frame_to_begin_middle_end_all(frame):
    if not frame.phoneme: return None
    # if frame.phoneme.duration < .025: return 'all'
    begin, middle, end = _split_phoneme_time(frame.phoneme)

    s1, e1 = frame.start,frame.end
    _phoneme = None
    _phoneme_duration = 0
    segments = begin, middle, end
    for segment in segments:
        s2, e2 = segment
        if general.overlap(s1,e1,s2,e2):
            duration = general.overlap_duration(s1,e1,s2,e2)
            if _phoneme and duration < _phoneme_duration: 
                continue
            _phoneme = segment
            _phoneme_duration = duration
    if _phoneme == begin: return 'begin'
    elif _phoneme == middle: return 'middle'
    elif _phoneme == end: return 'end'
    else: raise ValueError('unknown segment', segment, segments)

def combine_count_dicts(d, keys):
    output_d = {}
    for key in keys:
        count_dict = d[key]
        for phoneme, count in count_dict.items():
            if phoneme not in output_d.keys(): output_d[phoneme] = 0
            output_d[phoneme] += count
    output_d = dict_to_sorted_dict(output_d)
    return output_d
        
def get_vowels(d):
    p = _get_all_phonemes(d)
    vowels = p[p.index('eɪ'):-2]
    return vowels

def aggregate_vowel_codevector_phoneme_counts(d):
    '''aggregates phoneme counts for codevectors that are linked to vowels.
    for each vowel select a set of codevectors with highest count for that vowel.
    aggregate the phoneme counts for those codevectors.
    do this for both the stressed and unstressed version of the vowel
    '''
    phonemes = _get_all_phonemes(d)
    vowels = get_vowels(d)
    m = compute_phoneme_conditional_probability_matrix(d)
    row_index_max_value = np.argmax(m, axis=0)
    all_keys = list(d.keys())
    output_d = {}
    for vowel in vowels:
        index = phonemes.index(vowel)
        vowel_indices = np.where(row_index_max_value == index)[0]
        keys = [all_keys[i] for i in vowel_indices]
        output_d[vowel] = combine_count_dicts(d, keys)
    return output_d
        
def phoneme_count_dict_to_stress_no_stress(input_d):
    output_d = {'stress':0, 'no_stress':0}
    for phoneme, count in input_d.items():
        if '_stressed' in phoneme: output_d['stress'] += count
        else: output_d['no_stress'] += count
    return output_d

def _aggregate_phoneme_counts_to_stress_no_stress(input_d):
    output_d = {'stress':{}, 'no_stress':{}}
    for phoneme, count_dict in input_d.items():
        name = 'stress' if '_stressed' in phoneme else 'no_stress'
        temp = phoneme_count_dict_to_stress_no_stress(count_dict)
        for k, count in temp.items():
            if k not in output_d[name].keys(): output_d[name][k] = 0
            output_d[name][k] += count
    return output_d

def ground_truth_hyp_dict_to_classification_report(input_d):
    from sklearn.metrics import classification_report, matthews_corrcoef
    gt, hyp = [], []
    for k, v in input_d.items():
        for kk, vv in v.items():
            gt.extend([k] * vv)
            hyp.extend([kk] * vv)
    print(classification_report(gt, hyp))
    print('matthews correlation coefficient',matthews_corrcoef(gt, hyp))
    return gt, hyp

def classification_report_codevector_vowel_stress(d):
    o = aggregate_vowel_codevector_phoneme_counts(d)
    o = _aggregate_phoneme_counts_to_stress_no_stress(o)
    gt, hyp = ground_truth_hyp_dict_to_classification_report(o)
    return gt, hyp
        
    

    

