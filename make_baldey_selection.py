# to select data for the experiment described in issue
# https://github.com/martijnbentum/stress-miniature-succotash/issues/3
# This script will select the data from the baldey dutch lexical decision dataset 

import word
import random
from pathlib import Path
import shutil
import json


def _analyze_annotation(annotator,annotation_filename = ''):
    if not annotation_filename:
        f = '/Users/martijn.bentum/baldey_annotate/recordings/verkwaan.TextGrid'
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

def analyze_annotations(annotator, directory = '', output_filename = '',
    save = False):
    if not directory:
        p = Path('/Users/martijn.bentum/baldey_annotate/recordings/')
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
    goal_dir = '', w = None):
    if not w: 
        w = word.Words()
    if not filename:
        filename = f'baldey_syl-{n_syllables}_word-{n}.txt'
    if not goal_dir: goal_dir = '/Users/martijn.bentum/baldey_annotate/'
    words, non_words = select_words_nonwords(n = n, n_syllables = n_syllables,
        w = w)
    dataset = write_to_file(words, non_words, goal_dir + filename)
    copy_audio_files_words(words + non_words, goal_dir + 'recordings/')
    return dataset


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
    n_syllables = 2, w = None):
    # Select n words and n non-words
    if words is None or non_words is None:
        words, non_words = get_words_nonwords(n_syllables, w = w)
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