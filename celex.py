import locations
import phonemes

class Celex:
    def __init__(self, language = 'eng'):
        self.language = language
        self._set_data()

    def _set_data(self):
        if self.language == 'eng':
            self.data = open_cd(locations.celex_english_phonology_file)
        self._set_words()

    def _set_words(self):
        self.words = []
        self.word_dict = {}
        for line in self.data:
            word = Word(line)
            if not word.ok: continue
            self.words.append(word)
            self.word_dict[word.word] = word

    def get_word(self,word):
        return self.word_dict[word]

class Word:
    def __init__(self, line):
        self.line = line
        self.ok = True
        if len(line) > 7:self._set_info()
        else:self.ok = False
            

    def _set_info(self):
        self.number = self.line[0]
        self.word = self.line[1]
        self.cob = int(self.line[2])
        self.n_pronounciations = int(self.line[3])
        self.pronounciation_status = self.line[4]
        self.disc = self.line[5]
        self.cv = self.line[6]
        self.celex = self.line[7]
        self._extract_stress_pattern()
        self._compute_n_phonemes()

    def __repr__(self):
        m = self.number + ' ' + self.word + ' ' + self.disc
        m += ' ' + self.cv+ ' ' + self.celex + ' ' + self.stress_pattern
        return m

    def _extract_stress_pattern(self):
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
        self.n_phonemes = 0
        for char in self.disc:
            if char not in ["'",'"','-']: self.n_phonemes += 1

    @property
    def arpabet_syllables(self):
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
        if not hasattr(self,'_ipa'): 
            self._ipa = []
            for char in self.disc:
                if char in ['"',"'"]: continue
                if char == '-': self._ipa.append( char )
                else: self._ipa.append( phonemes.disc_to_ipa[char] )
        return ' '.join([p for p in self._ipa if p != '-'])

    @property
    def arpabet(self):
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
        
