import itertools
import locations
import os
import shutil
import descriptive_statistics as ds

def _syllable_to_dataset_line(syllable):
    s = syllable
    x = []
    x.append(s.ipa)
    x.append(str(s.stressed))
    x.append(s.stress) 
    x.append(str(s.start_time))
    x.append(str(s.end_time))
    x.append(s.word.audio_filename.split('/')[-1])
    x.append(s.vowel.ipa)
    x.append(str(s.vowel.start_time))
    x.append(str(s.vowel.end_time))
    return x

def copy_audio_file_to_dataset_directory(syllable, directory = None):
    if not directory: 
        directory = locations.mald_variable_stress_syllable_directory
    d = directory
    filename = syllable.word.audio_filename
    new_filename = d + filename.split('/')[-1]
    shutil.copy(filename,new_filename)

def _save_dataset_to_file(dataset, filename):
    with open(filename,'w') as f:
        f.write('\n'.join(['\t'.join(x) for x in dataset]))

def make_mald_variable_stress_syllable(sd = None, mald_syllable_dict = None,
    w = None, save = False):
    d = locations.mald_variable_stress_syllable_directory
    os.makedirs(d,exist_ok=True)
    if not sd: 
        if not mald_syllable_dict: 
            mald_syllable_dict = ds.mald_syllable_dict(w = w)
        _,sd = ds.stress_variability_mald(mald_syllable_dict,50,0.05,
            n_include=None)
    temp = [x['syllables'] for x in sd.values()]
    syls = list(itertools.chain(*temp))
    header = 'syllable_ipa stressed stress start_time end_time'
    header += ' word_audio_filename vowel_ipa vowel_start_time vowel_end_time'
    header = header.split()
    [copy_audio_file_to_dataset_directory(s,d) for s in syls]
    data, no_vowel, error = [], [], []
    for syllable in syls:
        if not syllable.vowel: 
            no_vowel.append(syllable)
            continue
        line = _syllable_to_dataset_line(syllable)
        if None in line: 
            error.append(syllable)
            continue
        data.append(line)
    if save: 
        dataset = [header] + data
        filename = d + 'mald_variable_stress_syllable.tsv'
        _save_dataset_to_file(dataset,filename)
    return header, data, syls, no_vowel, error

def make_mald_all_words_stress_syllable(w = None, save = False):
    mald_syllable_dict = ds.mald_syllable_dict(w = w)
    _,sd = ds.stress_variability_mald(mald_syllable_dict,1,1,n_include=None)
    header,data, syls, no_vowel, error = make_mald_variable_stress_syllable(sd, 
        save = False)
    dataset = [header] + data
    filename = '../mald_all_words_stress_syllable.tsv'
    if save: _save_dataset_to_file(dataset,filename)
    return header, data, syls, no_vowel, error

    
