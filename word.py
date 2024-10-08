import align_phonemes
import celex
import coolest
import copy
import json
import formants
import frequency_band
import locations
import make_syllabels_with_prosodic as mswp
import metadata
import os
import phoneme_mapper as pm
from progressbar import progressbar
import time
import utils

class Words:
    def __init__(self, load_datatsets = None, english_celex = None, 
            dutch_celex = None,):
        self._set_datasets(load_datatsets)
        self.word_to_filenames = metadata.word_to_filenames_dict()
        if not english_celex:english_celex = celex.Celex('english')
        if not dutch_celex: dutch_celex = celex.Celex('dutch')
        self.english_celex = english_celex
        self.dutch_celex = dutch_celex
        self.english_phoneme_mapper = pm.Mapper('english')
        self.dutch_phoneme_mapper = pm.Mapper('dutch')
        self._make_words()

        
    def _set_datasets(self, load_datatsets):
        if not load_datatsets: load_datatsets = 'baldey,mald'.split(',')
        if type(load_datatsets) == str: 
            if ',' in load_datatsets:load_datatsets = load_datatsets.split(',')
            else: load_datatsets = [load_datatsets]
        self.dataset_names = load_datatsets

        if 'baldey' in self.dataset_names:
            self.baldey_word_set = metadata.baldey_word_set()
            self.baldey_data = metadata.baldey_word_data()
            self.baldey_header = metadata.baldey_header()
        if 'mald' in self.dataset_names:
            self.mald_word_set = metadata.mald_word_set()
            self.mald_data = metadata.mald_word_data()
            self.mald_header = metadata.mald_word_header()
        if 'coolest' in self.dataset_names:
            self.coolest_word_set = metadata.coolest_word_set()
            self.coolest_data = metadata.coolest_word_data()
            self.coolest_header = metadata.coolest_word_header()

    def _make_words(self):
        self.words = []
        for name in self.dataset_names:
            if name == 'baldey': 
                word_index = 9
                language = 'dutch'
            elif name == 'mald': 
                word_index = 0
                language = 'english'
            else:
                word_index = 2
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
        elif self.dataset == 'mald': self._set_mald()
        elif self.dataset == 'coolest': self._set_coolest()
        else: raise ValueError(self.dataset,'unknown dataset')
        self._set_table()
        if self.dataset == 'mald':self._make_mald_syllables()
        if self.dataset == 'baldey': self._make_baldey_syllables()

    def _set_coolest(self):
        self.is_word = True
        self.n_syllables = 2
        self.audio_filename = self.d['filename']
        textgrid,table = coolest.get_textgrid_table_filename(self.d['filename'])
        self.textgrid_filename = textgrid
        self.table_filename = table
        self.language = 'dutch'
        self.phoneme_mapper = self.words.dutch_phoneme_mapper
        self.phoneme_transcription = ''
        self.celex = self.words.dutch_celex
        try: self.celex_word = self.celex.get_word(self.word)
        except KeyError: self.celex_word = None

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
        separator = ',' if self.dataset == 'coolest' else '\t'
        self.table = Table(self.table_filename, self, separator = separator)

    def _make_mald_syllables(self):
        self.syllable_error = False
        if not self.is_word: self.syllable_error = True
        elif hasattr(self,'celex_word') and self.celex_word:
            make_mald_syllables_with_celex(self)
        else: 
            try:make_mald_syllables_with_prosodic(self)
            except AssertionError: self.syllable_error = True
        if not hasattr(self,'syllables') or not self.syllables:
            self.syllable_error = True

    def _make_baldey_syllables(self):
        self.syllable_error = False
        if hasattr(self,'celex_word') and self.celex_word:
            make_baldey_syllables_with_celex(self)
        else: self.syllable_error = True

    @property
    def audio_info(self):
        if hasattr(self,'_audio_info'): return self._audio_info
        if self.dataset == 'baldey': raise ValueError('not implemented')
        elif self.dataset == 'coolest':
            self._audio_info = []
            ai = coolest.load_audio_info()
            for audio_filename, audio_info in ai.items():
                if coolest.filename_to_word(audio_filename) == self.word:
                    self._audio_info.append( audio_info )
        elif self.dataset == 'mald':
            self.audio_info_filename = locations.mald_audio_infos
            self.audio_info_filename += self.word.upper() + '.json'
            self._audio_info = json.load(open(self.audio_info_filename))
            self._audio_info['sample_rate']=int(self._audio_info['sample_rate'])
            self._audio_info['nchannels'] = int(self._audio_info['nchannels'])
        return self._audio_info

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
        if self.dataset == 'coolest':
            to_ipa = self.phoneme_mapper.sampa_to_ipa
            phonemes = self.phoneme_transcription
        self._ipa = []
        for phoneme in phonemes:
            self._ipa.append( to_ipa[phoneme] )
        return ' '.join(self._ipa)

    @property
    def signal(self):
        if hasattr(self,'_signal'): return self._signal
        sample_rate = self.audio_info['sample_rate']
        self._signal, _ = frequency_band.load_audio_file(self.audio_filename,
            sample_rate)
        return self._signal

    @property
    def formants(self):
        if hasattr(self,'_formants'): return self._formants
        self._formants = formants.Formants(self)
        return self._formants
            
class Table:
    def __init__(self, filename, word = None, separator = '\t'):
        self.filename = filename
        self.word = word
        if word: self.dataset = word.dataset
        else: self.dataset = None
        self.separator = separator
        self.table = open_table(filename, separator = separator)
        self._make_phonemes()

        self.n_phonemes = len(self.phonemes)
        self.phonemes_list = [p.phoneme for p in self.phonemes]
        self.phonemes_str = ' '.join(self.phonemes_list)

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
        if not self.word: word = ''
        else: word = self.word.word
        m = 'table| ' + word + ' ' + str(round(self.duration,2))
        return m

    def _make_phonemes(self):
        if self.word and 'speech_condition' in self.word.d.keys():
            speech_condition = self.word.d['speech_condition']
        else: speech_condition = None
        if self.dataset =='coolest' and speech_condition == 'sentence': 
            return self._make_phonemes_coolest()
        self.phonemes = []
        phoneme_index = 0
        for line in self.table:
            if line[1] not in  ['phone','segmentation','MAU']: continue
            if self.dataset == 'coolest' and line[2] == '<p:>': continue
            # if line[2] == 'sp': continue
            phoneme = Phoneme(line, self, phoneme_index)
            if phoneme.phoneme == 'sp': continue
            self.phonemes.append(phoneme)
            phoneme_index += 1

    def _make_phonemes_coolest(self):
        phoneme_code = 'MAU'
        word_line,word_maus = coolest.get_word_line_in_table(self.table, 
            self.word.word)
        start, end = word_maus[0], word_maus[-1]
        self.word_line, self.word_maus = word_line, word_maus
        self.phonemes = []
        self.syllable_lines = []
        phoneme_index = 0
        for line in self.table:
            if 'Syll' in line[1] and line not in self.syllable_lines:
                if line[0] < word_line[0] or line[-1] > word_line[-1]: 
                    pass
                else: self.syllable_lines.append(line)
                continue
            if line[1] != phoneme_code: continue
            if line[2] == '<p:>': continue
            if line[0] < start: continue
            if line[-1] > end: continue
            phoneme = Phoneme(line, self, phoneme_index)
            self.phonemes.append(phoneme)
            phoneme_index += 1

class Syllable:
    def __init__(self, phonemes, stress, index, word, source):
        self.phonemes = phonemes
        self.stress = stress
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

    @property
    def stressed(self):
        return self.stress == 'primary'

    @property
    def vowel(self):
        vowel = []
        for phoneme in self.phonemes:
            if phoneme.phoneme_type == 'vowel': vowel.append(phoneme)
        if not vowel: return None
        if len(vowel) > 1:
            for i,phoneme in enumerate(vowel):
                if i >= len(vowel) -1: break
                if not phoneme.phoneme_index == vowel[i+1].phoneme_index - 1:
                    #something is wrong do not return a vowel
                    return None
            v = copy.copy(vowel[0])
            for phoneme in vowel[1:]:
                v.phoneme += ' ' + phoneme.phoneme
            v.start_time = vowel[0].start_time
            v.end_time = vowel[-1].end_time
            v.duration = v.end_time - v.start_time
            vowel = v
        else: vowel = vowel[0]
        return vowel

    @property
    def signal(self):
        if hasattr(self,'_signal'): return self._signal
        sample_rate = self.word.audio_info['sample_rate']
        start,end = make_start_end_index(self.start_time,self.end_time, 
            sample_rate)
        self._signal = self.word.signal[start:end]
        return self._signal
            

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
        if not self.ipa: m = self.phoneme + '='
        else: m = self.ipa.ljust(4) 
        m += '| '+ str(self.phoneme_index) + ' | '
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
        if self.line[1] == 'silence': return 'silence'
        if self.table.dataset == 'mald':
            d = self.table.word.phoneme_mapper.arpabet_to_ipa
        elif self.table.dataset == 'baldey':
            d = self.table.word.phoneme_mapper.baldey_to_ipa
        elif self.table.dataset == 'coolest':
            d = self.table.word.phoneme_mapper.baldey_to_ipa
        if self.phoneme in d.keys():
            return d[self.phoneme]
        
    @property
    def disc(self):
        if self.table.dataset == 'mald':
            d = self.table.word.phoneme_mapper.arpabet_to_disc
        elif self.table.dataset == 'baldey':
            d = self.table.phoneme_mapper.baldey_to_disc
        elif self.table.dataset == 'coolest':
            d = self.table.word.phoneme_mapper.baldey_to_disc
        if self.phoneme in d.keys():
            return d[self.phoneme]
        else:
            d = self.table.word.phoneme_mapper.ipa_to_disc
            if self.ipa in d.keys():
                return d[self.ipa]

    @property
    def phoneme_type(self):
        if self.ipa == 'silence': return 'silence'
        if self.ipa in align_phonemes.vowels: return 'vowel'
        if self.ipa in align_phonemes.consonants: return 'consonant'
        raise ValueError(self.ipa,'phoneme type not found')

    @property
    def signal(self):
        if hasattr(self,'_signal'): return self._signal
        sample_rate = self.table.word.audio_info['sample_rate']
        start,end = make_start_end_index(self.start_time,self.end_time, 
            sample_rate)
        self._signal = self.table.word.signal[start:end]
        return self._signal

    @property
    def f1_f2(self):
        if hasattr(self,'_f1_f2'): return self._f1_f2
        formants = self.table.word.formants
        self._f1_f2 = formants.f1_f2(self)
        return self._f1_f2

    @property
    def mean_f1_f2(self):
        if hasattr(self,'_mean_f1_f2'): return self._mean_f1_f2
        formants = self.table.word.formants
        self._mean_f1_f2 = formants.mean_f1_f2(self)
        return self._mean_f1_f2

    @property
    def intensity(self):
        if hasattr(self,'_intensity'): return self._intensity
        import stress_intensity_diff as sid
        self._intensity = sid.compute_praat_intensity(self.signal)
        return self._intensity

    @property
    def pitch(self):
        if hasattr(self,'_pitch'): return self._pitch
        import stress_pitch_diff
        word = self.table.word
        self._pitch = stress_pitch_diff.handle_vowel(word,self)
        return self._pitch

    @property
    def spectral_balance(self):
        if hasattr(self,'_spectral_balance'): return self._spectral_balance
        import frequency_band
        self._spectral_balance = frequency_band.get_four_fb_to_db(self.signal)
        return self._spectral_balance

    @property
    def accoustic_correlates(self):
        if hasattr(self,'_accoustic_correlates'): 
            return self._accoustic_correlates
        o = [self.intensity, self.duration, self.pitch]
        o.extend( self.mean_f1_f2) 
        o.extend(self.spectral_balance)
        self._accoustic_correlates = o
        return self._accoustic_correlates


        
        

def open_table(filename, separator = '\t'):
    with open(filename) as fin:
        t = fin.read().split('\n')
    output = []
    for line in t[1:]:
        if not line: continue
        line = line.split(separator)
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

def make_phoneme_example_dict(words = None, phonemes = None):
    if not words: words = Words().words
    if not phonemes: 
        phonemes = phoneme_mapper.ipa_mald_vowels 
        phonemes += phoneme_mapper.ipa_mald_consonants
    output= {}
    for phoneme in phonemes:
        for word in words:
            if phoneme in word.ipa:
                if phoneme not in output.keys():
                    output[phoneme] = {'stressed':{'index':[],'word':[]},
                        'unstressed':{'index':[],'word':[]}}
                for p in word.table.phonemes:
                    if p.ipa == phoneme:
                        index = p.phoneme_index
                        if p.stressed: k = 'stressed'
                        else: k = 'unstressed'
                        output[phoneme][k]['index'].append(index)
                        output[phoneme][k]['word'].append(word)
    return output

def make_phoneme_count_dict(words = None,example_dict = None, phonemes = None):
    if not example_dict:
        example_dict = make_phoneme_example_dict(words, phonemes)
    phonemes = list(example_dict.keys())
    output = {}
    for phoneme in phonemes:
        output[phoneme] = len(example_dict[phoneme]['unstressed']['word'])
        output[phoneme+'_stressed'] = len(example_dict[phoneme]['stressed']['word'])
    return output

    
    
def make_start_end_index(start_time, end_time, sample_rate):
    start = int(start_time * sample_rate)
    end = int(end_time * sample_rate)
    return start,end
