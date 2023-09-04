import metadata
import time

class Words:
    def __init__(self):
        self.baldey_word_set = metadata.baldey_word_set()
        self.mald_word_set = metadata.mald_word_set()
        self.baldey_data = metadata.baldey_word_data()
        self.mald_data = metadata.mald_word_data()
        self.baldey_header = metadata.baldey_header()
        self.mald_header = metadata.mald_word_header()

    def make_words(self):
        self.words = []
        for line in self.baldey_data:
            word = line[9]
            d = metadata.word_to_filenames(word, dataset_name = 'baldey')
            d['header'] = self.baldey_header
            d['metadata'] = line
            self.words.append(Word(**d))
        for line in self.mald_data:
            word = line[0]
            d = metadata.word_to_filenames(word,dataset_name = 'mald')
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

    def __repr__(self):
        m = self.word
        return m
    
    def _set_info(self):
        self.d = {}
        for md, column_name in zip(self.metadata, self.header):
            self.d[column_name] = md
        self.is_word = self.d['word_status']
        if self.dataset == 'baldey': self._set_baldey()
        else: self._set_mald()

    def _set_mald(self):
        self.n_syllables = self.d['n_syllables']
        self.duration = self.d['duration']
        self.pos = self.d['pos']
        self.phonemes = self.d['phoneme_transcription']

    def _set_baldey(self):
        self.n_syllables = self.d['Nword_syllables']
        self.duration = self.d['word_duration']
        self.pos = self.d['word_class']
        self.phonemes = self.d['transcription']
            

