# to select data for the experiment described in issue
# https://github.com/martijnbentum/stress-miniature-succotash/issues/3
# This script will select the data from the baldey dutch lexical decision dataset 

import word
import random
from pathlib import Path
import shutil
import json

stress_dir ='/Users/martijn.bentum/Documents/indeep/stress/'

def analyze_annotations(annotator, directory = '', output_filename = '',
    save = False):
    '''Analyze the annotations of an annotator and return the results in a json.
    annotator: str, the name of the annotator
    directory: str, the directory where the annotations are stored
    output_filename: str, the filename where the output should be stored
    '''
    if not directory:
        p = Path(stress_dir + 'baldey_annotate/recordings/')
    else: p = Path(directory)
    output = []
    for filename in p.glob('*.TextGrid'):
        output.append(_analyze_annotation(annotator, filename))
    if save:
        if not output_filename:
            output_filename = p / f'../{annotator}_annotations.json'
        print('Saving to', output_filename)
        with open(output_filename, 'w') as f:
            json.dump(output, f)
    return output

def make_baldey_selection(n = 100, n_syllables = 2, filename = '', 
    goal_dir = '', w = None, exclude_word_list = []):
    '''Select n words and n non-words from the baldey dataset 
    and write them to a file.
    n: int, the number of words and non-words to select
    n_syllables: int, the number of syllables the words 
        and non-words should have
    filename: str, the name of the file where the output should be stored
    goal_dir: str, the directory where the output should be stored
    w: Words object, the object containing the words from the baldey dataset
    exclude_word_list: list, a list of words that should be excluded from the
        selection
    '''
    if not w: 
        w = word.Words()
    if not filename:
        filename = f'baldey_syl-{n_syllables}_word-{n}.txt'
    if not goal_dir: goal_dir = '/Users/martijn.bentum/baldey_annotate/'
    words, non_words = select_words_nonwords(n = n, n_syllables = n_syllables,
        w = w, exclude_word_list = exclude_word_list)
    dataset = write_to_file(words, non_words, goal_dir + filename)
    copy_audio_files_words(words + non_words, goal_dir + 'recordings/')
    return dataset

def word_to_vowels(word):
    '''Return a list of vowels in a word; word is a Word object (word.py).'''
    output = []
    for phoneme in word.table.phonemes:
        if phoneme.ipa is None: continue
        if phoneme.phoneme_type == 'vowel':
            output.append(phoneme)
    return output

def load_dataset(filename = ''):
    '''Load the dataset from a file created with make_baldey_selection.'''
    if not filename:
        filename = stress_dir + 'baldey_annotate/'
        filename += 'baldey_syl-2_word-combined.txt'
    with open(filename, 'r') as f:
        output = [line.split('\t') for line in f.read().split('\n')]
    return output, filename

def dataset_to_words(dataset_filename = '', w = None):
    '''Add the word objects to the dataset.
    dataset_filename: str, name of the dataset
    w: Words object, the object containing the words from the baldey dataset
    '''
    ds, dataset_filename = load_dataset(dataset_filename)
    output = []
    for line in ds:
        if not line or line == ['']: continue
        word = w.get_word(line[0])
        word = [x for x in word if x.dataset == 'baldey']
        if len(word) > 1:
            print('Warning: multiple words found for', word)
        line.append(word[0])
        output.append(line)
    return ds ,dataset_filename

def add_vowel_times_to_dataset(dataset_filename = '', w = None, save = False):
    '''Add the vowel times to the dataset.
    '''
    ds, dataset_filename = dataset_to_words(dataset_filename, w)
    output = []
    for line in ds:
        if not line or line == ['']: continue
        word = line[-1]
        output_line = line[:-1]
        if not word: continue
        vowels = word_to_vowels(word)
        for vowel in vowels:
            output_line.append(vowel_to_info(vowel))
        output.append(output_line)
    if save:
        filename = dataset_filename.split('.txt')[0] + '_vowels.txt'
        with open(filename, 'w') as f:
            f.write('\n'.join(['\t'.join(line) for line in output]))
    return output

def vowel_to_info(vowel):
    '''Return a string with the information of a vowel.'''
    output = vowel.ipa + ',' + str(vowel.start_time) + ',' 
    output += str(vowel.end_time) 
    return output
    



def _analyze_annotation(annotator,annotation_filename = ''):
    if not annotation_filename:
        f = stress_dir + 'baldey_annotate/'
        f += 'recordings/verkwaan.TextGrid'
        annotation_filename = f
    with open(annotation_filename, 'r') as f:
        lines = f.read().split('\n')
    word, annotation = None, None
    for line in lines:
        if line.strip().startswith('text'):
            line = line.split('"')[1].strip('"')
            if '.wav' in line:
                assert annotation is None
                word = line.split('.wav')[0]
            else: 
                assert word is not None
                annotation = int(line)
        if word and annotation:
            return [annotator,word, annotation]



def copy_audio_files_words(words, goal_dir):
    for word in words:
        source = word.audio_filename
        destination = goal_dir + Path(word.audio_filename).name
        print('Copying', source, 'to', destination)
        shutil.copy(source, destination)

def get_words_nonwords(n_syllables = 2, w = None):
    # Load the data
    if not w:
        w = word.Words()
    baldey = [x for x in w.words if x.dataset == 'baldey']
    words = [x for x in baldey if x.is_word and x.n_syllables == n_syllables]
    non_words = [x for x in baldey if not x.is_word and 
        x.n_syllables == n_syllables]
    return words, non_words

def select_words_nonwords(words = None, non_words = None, n = 100,
    n_syllables = 2, w = None, exclude_word_list = []):
    # Select n words and n non-words
    if words is None or non_words is None:
        words, non_words = get_words_nonwords(n_syllables, w = w)
    words = [x for x in words if x.word not in exclude_word_list]
    non_words = [x for x in non_words if x.word not in exclude_word_list]
    words = [x for x in words if len(word_to_vowels(x)) == n_syllables]
    non_words = [x for x in non_words if len(word_to_vowels(x)) == n_syllables]
    selected_words = random.sample(words, n)
    selected_non_words = random.sample(non_words, n)
    return selected_words, selected_non_words

def handle_word(word):
    # Create a line with word info for the output file
    word_status = 'word' if word.is_word else 'non-word'
    line = word.word + '\t' + word.ipa + '\t'
    line += word_status + '\t' + str(word.n_syllables) + '\t'
    if hasattr(word, 'syllables'):
        line += ' - '.join([syllable.ipa for syllable in word.syllables]) + '\t'
        line += ' - '.join([str(syllable.stressed) for syllable in 
            word.syllables])
    else: line += '\t'
    p =  Path(word.audio_filename)
    line += '\t' + p.resolve().as_posix()
    line += '\t' + p.name
    return line

def write_to_file(words, non_words, filename):
    # Write the selected words and non-words info to a file
    output = []
    for word in words:
        line = handle_word(word)
        output.append(line)
    for word in non_words:
        line = handle_word(word)
        output.append(line)
    with open(filename, 'w') as f:
        f.write('\n'.join(output))
    return output
