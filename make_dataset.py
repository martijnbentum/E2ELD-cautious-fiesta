import itertools
import locations
import os
import shutil

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

def move_audio_file_to_dataset_directory(syllable, directory = None):
    if not directory: 
        directory = locations.mald_variable_stress_syllable_directory
    d = directory
    filename = syllable.word.audio_filename
    new_filename = d + filename.split('/')[-1]
    shutil.copy(filename,new_filename)

def make_mald_variable_stress_syllable(sd = None):
    d = locations.mald_variable_stress_syllable_directory
    os.makedirs(d,exist_ok=True)
    if not sd: _,sd = ds.stress_variability_mald(d,50,0.05,n_include=None)
    temp = [x['syllables'] for x in sd.values()]
    syls = list(itertools.chain(*temp))
    header = 'syllable_ipa stressed stress start_time end_time'
    header += ' word_audio_filename vowel_ipa vowel_start_time vowel_end_time'
    header = header.split()
    [move_audio_file_to_dataset_directory(s,d) for s in syls]
    data = [_syllable_to_dataset_line(s) for s in syls]
    dataset = [header] + data
    filename = d + 'mald_variable_stress_syllable.tsv'
    with open(filename,'w') as f:
        f.write('\n'.join(['\t'.join(x) for x in dataset]))
    return header, data

    
