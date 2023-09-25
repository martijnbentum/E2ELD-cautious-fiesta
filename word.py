import align_phonemes
import celex
import locations
import make_syllabels_with_prosodic as mswp
import metadata
import os
# import phonemes
import phoneme_mapper as pm
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
        self.english_celex = celex.Celex('english')
        self.dutch_celex = celex.Celex('dutch')
        self.english_phoneme_mapper = pm.Mapper('english')
        self.dutch_phoneme_mapper = pm.Mapper('dutch')
        self._make_words()


    def _make_words(self):
        self.words = []
        self.dataset_names = 'baldey,mald'.split(',')
        for name in self.dataset_names:
            if name == 'baldey': 
                word_index = 9
                language = 'dutch'
            elif name == 'mald': 
                word_index = 0
                language = 'english'
            self._handle_data(name,word_index,language)

    def _handle_data(self,name,word_index,language):
            data = getattr(self,name + '_data')
            print('handling',name)
            for line in progressbar(data):
                word = line[word_index]
                d = self.word_to_filenames[name][word]
                d['header'] = getattr(self,name + '_header')
                d['metadata'] = line
                d['words'] = self
                d['language'] = language
                d['dataset'] = name
                self.words.append(Word(**d))

    def get_word(self,word):
        output = []
        for w in self.words:
            if w.word == word: output.append(w)
        return output


class Word:
    def __init__(self, word, audio_filename, textgrid_filename, 
        metadata, header, words, language, dataset):
        self.word = word
        self.audio_filename = audio_filename
        self.textgrid_filename = textgrid_filename
        self.metadata = metadata
        self.header = header
        self.words = words
        self.language = language
        self.dataset = dataset
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
        if self.dataset == 'mald':self._make_mald_syllables()
        if self.dataset == 'baldey': self._make_baldey_syllables()

    def _set_mald(self):
        self.is_word = self.d['word_status']
        self.n_syllables = self.d['n_syllables']
        self.duration = self.d['duration']
        self.pos = self.d['pos']
        self.phoneme_transcription = self.d['phoneme_transcription']
        self.language = 'english'
        self.phoneme_mapper = self.words.english_phoneme_mapper
        self.table_filename = locations.mald_table_directory
        self.table_filename+= self.audio_filename.split('/')[-1].split('.')[0]
        self.table_filename += '.csv'
        if self.is_word:
            self.celex = self.words.english_celex
            try: self.celex_word = self.celex.get_word(self.word)
            except KeyError: self.celex_word = None
        else: self.celex_word = None
        self.n_phonemes = len(self.phoneme_transcription.split(' '))
        if self.is_word:
            self.prosodic = mswp.load_json(self.word)
        else: self.prosodic = None

    def _set_baldey(self):
        if self.d['word_status'] == 'word': self.is_word = True
        else: self.is_word = False
        self.n_syllables = self.d['Nword_syllables']
        self.duration = self.d['word_duration']
        self.pos = self.d['word_class']
        self.phoneme_transcription = self.d['transcription']
        self.phoneme_mapper = self.words.dutch_phoneme_mapper
        self.language = 'dutch'
        self.table_filename = locations.baldey_tables_directory
        self.table_filename+= self.audio_filename.split('/')[-1].split('.')[0]
        self.table_filename += '.csv'
        if self.is_word:
            self.celex = self.words.dutch_celex
            try: self.celex_word = self.celex.get_word(self.word)
            except KeyError: self.celex_word = None
        else: self.celex_word = None

    def _set_table(self):
        if not os.path.isfile(self.table_filename): return
        self.table = Table(self.table_filename, self)

    def _make_mald_syllables(self):
        self.syllable_error = False
        if not self.is_word: self.syllable_error = True
        elif hasattr(self,'celex_word') and self.celex_word:
            make_mald_syllables_with_celex(self)
        else: 
            try:make_mald_syllables_with_prosodic(self)
            except AssertionError: self.syllable_error = True

    def _make_baldey_syllables(self):
        self.syllable_error = False
        if hasattr(self,'celex_word') and self.celex_word:
            make_baldey_syllables_with_celex(self)
        else: self.syllable_error = True

    @property
    def ipa(self):
        if hasattr(self,'_ipa'): return ' '.join(self._ipa)
        if self.dataset == 'baldey':
            to_ipa = self.phoneme_mapper.disc_to_ipa
            phonemes = self.phoneme_transcription
        if self.dataset == 'mald':
            to_ipa = self.phoneme_mapper.arpabet_to_ipa
            p = self.phoneme_transcription.split(' ')
            phonemes = [utils.remove_numeric(x) for x in p]
        self._ipa = []
        for phoneme in phonemes:
            self._ipa.append( to_ipa[phoneme] )
        return ' '.join(self._ipa)
            
class Table:
    def __init__(self, filename, word = None):
        self.filename = filename
        self.word = word
        self.table = open_table(filename)
        self._make_phonemes()
        if self.phonemes:
            self.start = self.phonemes[0].start_time
            self.end = self.phonemes[-1].end_time
            self.duration = self.end - self.start
            self.ok = True
        else:
            self.start = None 
            self.end = None
            self.duration = None
            self.ok = False 
            
    def __repr__(self):
        m = 'table| ' + self.word.word + ' ' + str(round(self.duration,2))
        return m

    def _make_phonemes(self):
        self.phonemes = []
        phoneme_index = 0
        for line in self.table:
            if line[1] not in  ['phone','segmentation']: continue
            # if line[2] == 'sp': continue
            phoneme = Phoneme(line, self, phoneme_index)
            if phoneme.phoneme == 'sp': continue
            self.phonemes.append(phoneme)
            phoneme_index += 1
        self.n_phonemes = len(self.phonemes)
        self.phonemes_list = [p.phoneme for p in self.phonemes]
        self.phonemes_str = ' '.join(self.phonemes_list)

class Syllable:
    def __init__(self, phonemes, stress, index, word, source):
        self.phonemes = phonemes
        self.stress = stress
        self.stressed = self.stress == 'primary'
        self.start_time = self.phonemes[0].start_time
        self.end_time = self.phonemes[-1].end_time
        self.duration = self.end_time - self.start_time
        self.index = index
        self.word = word
        self.dataset = word.dataset
        self.source = source
        self.phonemes_str = ' '.join([p.phoneme for p in self.phonemes])

    def __hash__(self):
        return hash(self.ipa)

    def __eq__(self,other):
        if not type(self) == type(other): return False
        return self.ipa == other.ipa

    
    def __repr__(self):
        m = 'Syl| '
        m += self.ipa.ljust(9) + '| ' 
        m += str(round(self.duration,2)).ljust(5)
        m += '| ' + self.stress.ljust(10)
        m += '| i: ' + str(self.index)
        m += ' | ' + self.word.word
        m += ' | ' + self.source
        return m

    def __str__(self):
        m = 'Syllable| '
        m += self.phonemes_str.ljust(9) + '| '  
        m += self.ipa.ljust(9) + '| (' 
        m += str(round(self.start_time,2)).ljust(5) + '- '
        m += str(round(self.end_time,2)).ljust(4) + ') '
        m += str(round(self.duration,2)).ljust(4)
        m += ' | ' + self.stress.ljust(10)
        m += '| ' + self.source
        m += ' | ' + str(self.index)
        m += ' | ' + self.word.word
        return m

    @property
    def ipa(self):
        if hasattr(self,'_ipa'): return ' '.join(self._ipa)
        if self.dataset == 'baldey':
            to_ipa = self.word.phoneme_mapper.baldey_to_ipa
            phonemes = self.phonemes_str.split(' ')
        if self.dataset == 'mald':
            to_ipa = self.word.phoneme_mapper.arpabet_to_ipa
            p = self.phonemes_str.split(' ')
            phonemes = [utils.remove_numeric(x) for x in p]
        self._ipa = []
        for phoneme in phonemes:
            self._ipa.append( to_ipa[phoneme] )
        return ' '.join(self._ipa)

class Phoneme:
    def __init__(self, line, table, phoneme_index):
        self.line = line
        self.table = table
        self.phoneme_index = phoneme_index
        self.start_time = line[0]
        self.end_time = line[-1]
        self.duration = self.end_time - self.start_time
        self._set_phoneme()
        self.syllable_index = None
    
    def __repr__(self):
        m = self.ipa.ljust(4) + '| '+ str(self.phoneme_index) + ' | '
        m += str(self.syllable_index) + ' | '
        m += str(self.stressed) + ' | '
        m += ' ' + str(round(self.start_time,2)).ljust(5) 
        m += '- ' + str(round(self.end_time,2))
        return m

    def _set_phoneme(self):
        if self.table.word.dataset == 'mald':
            self.phoneme = utils.remove_numeric(self.line[2])
        else:
            self.phoneme = self.line[2]
        self.stress_number = utils.get_number(self.line[2])
        if self.stress_number == 1: self.stressed = True
        else: self.stressed = False
        

    @property
    def ipa(self):
        if self.table.word.dataset == 'mald':
            d = self.table.word.phoneme_mapper.arpabet_to_ipa
        else:
            d = self.table.word.phoneme_mapper.baldey_to_ipa
        if self.phoneme in d.keys():
            return d[self.phoneme]
        
    @property
    def disc(self):
        if self.table.word.dataset == 'mald':
            d = self.table.word.phoneme_mapper.arpabet_to_disc
        else:
            d = self.table.word.phoneme_mapper.baldey_to_disc
        if self.phoneme in d.keys():
            return d[self.phoneme]
        else:
            d = self.table.word.phoneme_mapper.ipa_to_disc
            if self.ipa in d.keys():
                return d[self.ipa]
        
        

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
        


def make_mald_syllables_with_celex(word):
    word.syllables = []
    # assert word.table.n_phonemes == word.celex_word.n_phonemes
    if word.table.n_phonemes != word.celex_word.n_phonemes:
        handle_unequal_phonemes_mald(word)
        return
    n_phonemes = word.celex_word.n_phonemes
    phoneme_index = 0
    arpabet_syllables = word.celex_word.arpabet_syllables
    for syllable_index,syllable in enumerate(arpabet_syllables):
        phonemes = []
        for _ in range(len(syllable)):
            phoneme = word.table.phonemes[phoneme_index]
            phoneme.syllable_index = syllable_index
            phonemes.append(phoneme)
            phoneme_index += 1
        stress = x=word.celex_word.stress_list[syllable_index]
        syllable = Syllable(phonemes,stress, syllable_index, word, 'celex')
        word.syllables.append(syllable)

def _check_mald_word_syllable_indices(word):
    for i, syllable in enumerate(word.syllables):
        if i == syllable.index: continue
        syllable.index = i
        for phoneme in syllable.phonemes:
            phoneme.syllable_index = i

def handle_unequal_phonemes_mald(word):
    align_phonemes.set_textgrid_phonemes_syllable_index_mald(word)
    syllable_index = 0
    phonemes = []
    word_has_stress = False
    for i,phoneme in enumerate(word.table.phonemes):
        # print(i,word)
        if syllable_index != phoneme.syllable_index:
            syllable = Syllable(phonemes,stress, syllable_index,word, 'celex ul')
            word.syllables.append(syllable)
            phonemes = []
        syllable_index = phoneme.syllable_index
        if word.syllable_index_fixed:
            if syllable_index < len(word.celex_word.stress_list) - 1:
                stress = word.celex_word.stress_list[syllable_index+1]
            if not word_has_stress and i >= len(word.table.phonemes):
                stress = 'primary'
        else:
            stress = word.celex_word.stress_list[syllable_index]
        if stress == 'primary': word_has_stress = True
        phonemes.append(phoneme)
    if phonemes:
        syllable = Syllable(phonemes,stress, syllable_index,word, 'celex ul')
        word.syllables.append(syllable)
    if not word_has_stress and word.syllable_index_fixed: 
        word.syllables[0].stress = 'primary'
    _check_mald_word_syllable_indices(word)

def make_mald_syllables_with_prosodic(word):
    d = mswp.load_json(word.word)
    n_phonemes_prosodic = mswp.dict_to_n_phonemes(d)
    # print(word.table.n_phonemes,n_phonemes_prosodic,word)
    assert word.table.n_phonemes == n_phonemes_prosodic
    word.syllables = []
    phoneme_index = 0
    for syllable_index,syllable in enumerate(d['syllables']):
        phonemes = []
        for _ in range(len(syllable['arpabet'].split(' '))):
            phoneme = word.table.phonemes[phoneme_index]
            phoneme.syllable_index = syllable_index
            phonemes.append(phoneme)
            phoneme_index += 1
        stress = syllable['stress_type']
        if stress == 'P':stress = 'primary'
        elif stress == 'S':stress = 'secondary'
        elif stress == 'U':stress = 'no stress'
        syllable = Syllable(phonemes,stress, syllable_index, word, 'prosodic')
        word.syllables.append(syllable)


            
def make_baldey_syllables_with_celex(word):
    assert word.table.n_phonemes == word.celex_word.n_phonemes
    n_phonemes = word.celex_word.n_phonemes
    word.syllables = []
    phoneme_index = 0
    ipa_syllables = word.celex_word.ipa_syllables
    for syllable_index,syllable in enumerate(ipa_syllables):
        phonemes = []
        for _ in range(len(syllable)):
            phoneme = word.table.phonemes[phoneme_index]
            phoneme.syllable_index = syllable_index
            phonemes.append(phoneme)
            phoneme_index += 1
        stress = x=word.celex_word.stress_list[syllable_index]
        syllable = Syllable(phonemes,stress, syllable_index, word, 'celex')
        word.syllables.append(syllable)
    
