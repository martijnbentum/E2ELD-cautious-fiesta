import locations
import phonemes

class Celex:
    def __init__(self, language = 'english'):
        self.language = language
        self._set_data()

    def _set_data(self):
        if self.language == 'english':
            self.data = open_cd(locations.celex_english_phonology_file)
            self.header = open_header('english')
        if self.language == 'dutch':
            self.data = open_cd(locations.celex_dutch_phonology_file)
            self.header = open_header('dutch')
        self._set_words()

    def _set_words(self):
        self.words = []
        self.word_dict = {}
        for line in self.data:
            word = Word(line,self)
            if not word.ok: continue
            self.words.append(word)
            self.word_dict[word.word] = word

    def get_word(self,word):
        return self.word_dict[word]

class Word:
    def __init__(self, line, celex):
        self.line = line
        self.celex = celex
        self.ok = True
        self._set_info()
            

    def _set_info(self):
        for column_name, column in zip(self.celex.header, self.line):
            setattr(self,column_name, column)
        '''
        self.number = self.line[0]
        self.word = self.line[1]
        self.cob = int(self.line[2])
        self.n_pronounciations = int(self.line[3])
        self.pronounciation_status = self.line[4]
        self.disc = self.line[5]
        self.cv = self.line[6]
        self.celex = self.line[7]
        '''
        self._extract_stress_pattern()
        self._compute_n_phonemes()

    def __repr__(self):
        m = self.id_number + ' ' + self.word + ' ' + self.disc
        m += ' ' + self.cv+ ' ' + self.celex + ' ' + self.stress_pattern
        return m

    def _extract_stress_pattern(self):
        if not hasattr(self,'disc'):
            self.ok = False
            return
        self.disc_syllables = self.disc.split('-')
        self.stress_list = []
        self.stress_pattern = ''
        for syllable in self.disc_syllables:
            if '"' in syllable:
                self.stress_list.append('secondary')
                self.stress_pattern += '2'
            elif "'" in syllable:
                self.stress_list.append('primary')
                self.stress_pattern += '1'
            else:
                self.stress_list.append('no stress')
                self.stress_pattern += '0'

    def _compute_n_phonemes(self):
        if not hasattr(self,'disc'): 
            self.ok = False
            return
        self.n_phonemes = 0
        for char in self.disc:
            if char not in ["'",'"','-']: self.n_phonemes += 1

    @property
    def arpabet_syllables(self):
        if not self.ok: return
        if hasattr(self,'_arpabet_syllables'): return self._arpabet_syllables
        self.arpabet
        self._arpabet_syllables = []
        syllable = []
        for phoneme in self._arpabet:
            if phoneme == '-': 
                if syllable: self._arpabet_syllables.append(syllable)
                syllable = []
            else: syllable.append(phoneme)
        if syllable: self._arpabet_syllables.append(syllable)
        return self._arpabet_syllables

    @property
    def ipa_syllables(self):
        if not self.ok: return
        if hasattr(self,'_ipa_syllables'): return self._ipa_syllables
        self.ipa
        self._ipa_syllables = []
        syllable = []
        for phoneme in self._ipa:
            if phoneme == '-': 
                if syllable: self._ipa_syllables.append(syllable)
                syllable = []
            else: syllable.append(phoneme)
        if syllable: self._ipa_syllables.append(syllable)
        return self._ipa_syllables

    @property
    def ipa(self):
        if not self.ok: return
        if not hasattr(self,'_ipa'): 
            self._ipa = []
            for char in self.disc:
                if char in ['"',"'"]: continue
                if char == '-': self._ipa.append( char )
                else: self._ipa.append( phonemes.disc_to_ipa[char] )
        return ' '.join([p for p in self._ipa if p != '-'])

    @property
    def arpabet(self):
        if not self.ok: return
        if not hasattr(self,'_arpabet'):
            self._arpabet= []
            for char in self.disc:
                if char in ['"',"'"]: continue
                if char == '-': self._arpabet.append( char )
                else: self._arpabet.append( phonemes.disc_to_arpabet[char] )
        return ' '.join([p for p in self._arpabet if p != '-'])


def open_cd(filename):
    with open(filename) as fin:
        t = fin.read().split('\n')
    output = []
    for line in t:
        output.append(line.split('\\'))
    return output
        
def open_header(language):
    f = locations.celex_directory + language + '_header'
    with open(f) as fin:
        header = fin.read().split('\n')
    return header
