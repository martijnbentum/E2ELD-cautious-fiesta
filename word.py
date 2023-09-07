import celex
import locations
import metadata
import os
import phonemes
from progressbar import progressbar
import time
import utils

class Words:
    def __init__(self):
        self.baldey_word_set = metadata.baldey_word_set()
        self.mald_word_set = metadata.mald_word_set()
        self.baldey_data = metadata.baldey_word_data()
        self.mald_data = metadata.mald_word_data()
        self.baldey_header = metadata.baldey_header()
        self.mald_header = metadata.mald_word_header()
        self.word_to_filenames = metadata.word_to_filenames_dict()
        self.celex = celex.Celex()
        self._make_words()

    def _make_words(self):
        self.words = []
        for line in self.baldey_data:
            word = line[9]
            d = self.word_to_filenames['baldey'][word]
            d['header'] = self.baldey_header
            d['metadata'] = line
            d['words'] = self
            self.words.append(Word(**d))
        for line in self.mald_data:
            word = line[0]
            d = self.word_to_filenames['mald'][word]
            d['header'] = self.mald_header
            d['metadata'] = line
            d['words'] = self
            self.words.append(Word(**d))


class Word:
    def __init__(self, word, audio_filename, textgrid_filename, 
        metadata, header, words):
        self.word = word
        self.audio_filename = audio_filename
        self.textgrid_filename = textgrid_filename
        self.metadata = metadata
        self.header = header
        self.words = words
        if len(self.header) == 50: self.dataset = 'baldey'
        else: self.dataset = 'mald'
        self._set_info()

    def __repr__(self):
        m = self.dataset + '| ' + self.word + ' | ' +str(self.is_word)
        m += ' | ' + self.ipa
        m += ' | ' + str(self.n_syllables)
        return m
    
    def _set_info(self):
        self.d = {}
        for md, column_name in zip(self.metadata, self.header):
            self.d[column_name] = md
        if self.dataset == 'baldey': self._set_baldey()
        else: self._set_mald()
        self._set_table()

    def _set_mald(self):
        self.is_word = self.d['word_status']
        self.n_syllables = self.d['n_syllables']
        self.duration = self.d['duration']
        self.pos = self.d['pos']
        self.phoneme_transcription = self.d['phoneme_transcription']
        self.language = 'english'
        self.ipa = phonemes.make_mald_ipa(self.phoneme_transcription)
        self.table_filename = locations.mald_table_directory
        self.table_filename += self.audio_filename.split('/')[-1].split('.')[0]
        self.table_filename += '.csv'
        if self.is_word:
            try: self.celex_word = self.words.celex.get_word(self.word)
            except KeyError: self.celex_word = None
        else: self.celex_word = None
        self.n_phonemes = len(self.phoneme_transcription.split(' '))

    def _set_baldey(self):
        if self.d['word_status'] == 'word': self.is_word = True
        else: self.is_word = False
        self.n_syllables = self.d['Nword_syllables']
        self.duration = self.d['word_duration']
        self.pos = self.d['word_class']
        self.phonemes = self.d['transcription']
        self.language = 'dutch'
        self.table_filename = ''

    def _set_table(self):
        if not os.path.isfile(self.table_filename): return
        self.table = Table(self.table_filename, self)
            
class Table:
    def __init__(self, filename, word = None):
        self.filename = filename
        self.word = word
        self.table = open_table(filename)
        self._make_phonemes()
        self.start = self.phonemes[0].start_time
        self.end = self.phonemes[-1].end_time
        self.duration = self.end - self.start

    def __repr__(self):
        m = 'table| ' + self.word.word + ' ' + str(round(self.duration,2))
        return m

    def _make_phonemes(self):
        self.phonemes = []
        for line in self.table:
            if line[1] != 'phone': continue
            phoneme = Phoneme(line, self)
            self.phonemes.append(phoneme)

class Syllable:
    def __init__(self, phonemes, stress):
        self.phonemes = phonemes
        self.stress = stress
        self.start_time = self.phonemes[0].start_time
        self.end_time = self.phonemes[-1].duration_time
        

class Phoneme:
    def __init__(self, line, table):
        self.line = line
        self.table = table
        self.start_time = line[0]
        self.end_time = line[-1]
        self.duration = self.end_time - self.start_time
        self._set_phoneme()
    
    def __repr__(self):
        m = self.phoneme.ljust(4) + str(self.stress_number) + ' | '
        m += ' ' + str(round(self.start_time,2)).ljust(5) 
        m += '- ' + str(round(self.end_time,2))
        return m

    def _set_phoneme(self):
        self.phoneme = utils.remove_numeric(self.line[2])
        self.stress_number = utils.get_number(self.line[2])
        if self.stress_number != 0: self.stressed = True
        else: self.stressed = False
        
        
        
        

def open_table(filename):
    with open(filename) as fin:
        t = fin.read().split('\n')
    output = []
    for line in t[1:]:
        if not line: continue
        line = line.split('\t')
        line[0] = float(line[0])
        line[-1] = float(line[-1])
        output.append(line)
    return output


def select_words(words, n_syllables = None, language = None, is_word = None):
    output = words
    if n_syllables:
        output = [word for word in output if word.n_syllables == n_syllables]
    if language:
        output = [word for word in output if word.language == language]
    if is_word:
        output = [word for word in output if word.is_word == is_word]
    return output
        
    pass



