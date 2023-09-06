import metadata
from progressbar import progressbar
import time

class Words:
    def __init__(self):
        self.baldey_word_set = metadata.baldey_word_set()
        self.mald_word_set = metadata.mald_word_set()
        self.baldey_data = metadata.baldey_word_data()
        self.mald_data = metadata.mald_word_data()
        self.baldey_header = metadata.baldey_header()
        self.mald_header = metadata.mald_word_header()
        self.word_to_filenames = metadata.word_to_filenames_dict()
        self._make_words()

    def _make_words(self):
        self.words = []
        for line in self.baldey_data:
            word = line[9]
            d = self.word_to_filenames['baldey'][word]
            d['header'] = self.baldey_header
            d['metadata'] = line
            self.words.append(Word(**d))
        for line in self.mald_data:
            word = line[0]
            d = self.word_to_filenames['mald'][word]
            d['header'] = self.mald_header
            d['metadata'] = line
            self.words.append(Word(**d))


class Word:
    def __init__(self, word, audio_filename, textgrid_filename, 
        metadata, header):
        self.word = word
        self.audio_filename = audio_filename
        self.textgrid_filename = textgrid_filename
        self.metadata = metadata
        self.header = header
        if len(self.header) == 50: self.dataset = 'baldey'
        else: self.dataset = 'mald'
        self._set_info()

    def __repr__(self):
        m = self.dataset + '| ' + self.word + ' ' +str(self.is_word)
        m += ' ' + str(self.n_syllables)
        return m
    
    def _set_info(self):
        self.d = {}
        for md, column_name in zip(self.metadata, self.header):
            self.d[column_name] = md
        if self.dataset == 'baldey': self._set_baldey()
        else: self._set_mald()

    def _set_mald(self):
        self.is_word = self.d['word_status']
        self.n_syllables = self.d['n_syllables']
        self.duration = self.d['duration']
        self.pos = self.d['pos']
        self.phonemes = self.d['phoneme_transcription']
        self.language = 'english'

    def _set_baldey(self):
        if self.d['word_status'] == 'word': self.is_word = True
        else: self.is_word = False
        self.n_syllables = self.d['Nword_syllables']
        self.duration = self.d['word_duration']
        self.pos = self.d['word_class']
        self.phonemes = self.d['transcription']
        self.language = 'dutch'
            

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

