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
            

