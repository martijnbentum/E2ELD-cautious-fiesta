'''
module to load the metadata for words
datasets:
baldey
mald
'''

import locations

def get_mald_word_metadata(word, data = None):
    '''get the metadata for a word in the mald dataset
    '''
    if not data: data = mald_word_data()
    for line in data:
        if line[0] == word: return line
    print('could not find',word,'in mald metadata')

def get_baldey_word_metadata(word, data = None):
    if not data: data = baldey_word_data()
    for line in data:
        if line[9] == word: return line
    print('could not find',word,'in baldey metadata')


# mald helper functions

def mald_word_header():
    '''lists all column names
    some names are cleaned up to be more readable
    '''
    h = 'word,wav_filename,phoneme_transcription,word_status,stress_pattern'
    h += ',n_syllables,n_phonemes,duration,orth_up,phon_nd,orth_nd,pos'
    h += ',all_pos,frequency_subtlex,frequency_coca,frequency_coca_spoken'
    h += ',frequency_google,phon_up,stress_cat,d_bet,phon_lev,n_morphemes'
    h += ',orth_lev'
    return h.split(',')

def mald_datatype_dict_header():
    '''maps the column name to the correct datatype.
    '''
    s = 'word,wav_filename,phoneme_transcription,stress_pattern,pos,all_pos'
    s += ',stress_cat,d_bet'
    s = s.split(',')
    i = 'n_syllables,n_phonemes,duration,orth_up,phon_nd,orth_nd'
    i += ',frequency_subtlex,frequency_coca,frequency_coca_spoken'
    i += ',frequency_google,phon_up,n_morphemes'
    i = i.split(',')
    f = 'phon_lev,orth_lev'.split(',')
    b = ['word_status']
    d = {}
    for datatype,column_names in zip([str,int,float,bool],[s,i,f,b]):
        for column_name in column_names:
            d[column_name] = datatype
    return d

def mald_word_data():
    '''load the file with the metadata for each word and non word in the mald
    dataset.
    converts values to the correct data type
    '''
    header = mald_word_header()
    datatypes = mald_datatype_dict_header()
    with open(locations.mald_word_data_filename) as fin:
        t = fin.read()
    temp = [x.split('\t') for x in t.split('\n')[1:] if x]
    output = []
    for line in temp:
        output_line = []
        for index,item in enumerate(line):
            item = item.strip('"')
            if item == 'NA': item = None
            else:
                column_name = header[index]
                if column_name == 'word_status':
                    if item == 'TRUE': item = True
                    else: item = False
                else:
                    item = datatypes[column_name](item)
            output_line.append(item)
        output.append(output_line)
    return output

# baldey helper functions

def baldey_columns():
    with open(locations.baldey_column_filename) as fin:
        t = fin.read().split('\n')
    d = {}
    for line in t[1:]:
        if not line: continue
        if not ': ' in line: d[line] = None
        else:
            name, explanation = line.split(': ')
            d[name] = explanation
    return d

def baldey_header(column_dict = None):
    if not column_dict: column_dict = baldey_columns()
    header = list(column_dict.keys())
    return header
    
def baldey_word_data():
    return baldey_data(only_unique_words = True)

def baldey_data(only_unique_words = False):
    all_words = baldey_word_set()
    with open(locations.baldey_data_filename) as fin:
        t = fin.read().split('\n')
    temp = [line.split(' ') for line in t[1:] if line]
    output = []
    header = baldey_header()
    datatypes= baldey_datatype_dict_header()
    found_words = set()
    for line in temp:
        word = line[header.index('word')]
        if only_unique_words and found_words == all_words:break
        if word in found_words: continue
        else: found_words.add(word)
        output_line = []
        for index, item in enumerate(line):
            if not item: continue
            column_name = header[index]
            datatype = datatypes[column_name]
            if item == '-': item = None
            elif datatype == bool:
                if item in ['correct','yes','unknown']:item = True
                elif item in ['incorrect','no','known']:item = False
            else: item = datatype(item)
            output_line.append(item)
        output.append(output_line)
    return output

def baldey_datatype_dict_header():
    s = 'subject,gender,hand,origin,dialect,diploma,word,response'
    s += ',stem,transcription,word_class,lip,fip,stressed_syll'
    s += ',morph_classification,tense,number,person,regularity,affix'
    s += ',stem1,stem2,compound_type'
    s = s.split(',')
    i = 'session,trial,age,RT,RTprev,Nphonemes,Nletters,Nstem_syllables'
    i += ',Nword_syllables,word_duration,CELEX_form_freq,CELEX_lemma_freq'
    i += ',CGN_form_freq,CGN_lemma_freq,CELEX_form_freq_stem1'
    i += ',CELEX_form_freq_stem2,CELEX_lemma_freq_stem1'
    i += ',CELEX_lemma_freq_stem2'
    i = i.split(',')
    f = 'lip.ms,fip.ms,rating'.split(',')
    b = 'word_status,response,inflected,initial_stress,final_stress'
    b += ',word_unknown,meaning_unknown'
    b = b.split(',')
    d = {}
    for datatype,column_names in zip([str,int,float,bool],[s,i,f,b]):
        for column_name in column_names:
            d[column_name] = datatype
    return d

def baldey_word_set():
    with open(locations.baldey_wordset_filename) as fin:
        t = fin.read().split('\n')
    return t

def mald_word_set():
    with open(locations.mald_wordset_filename) as fin:
        t = fin.read().split('\n')
    return t

def filename_to_word(filename):
    word = filename.split('/')[-1].split('.')[0].lower()
    return word

def word_to_filenames(word, dataset = 'baldey'):
    if dataset == 'baldey':
        fn_audio = locations.fn_baldey_audio
        fn_textgrids = locations.fn_baldey_textgrids
    else:
        fn_audio = locations.fn_mald_audio
        fn_textgrids = locations.fn_mald_textgrids
    d = {'word':word}
    for f in fn_audio:
        if filename_to_word(f) == word:
            d['audio_filename'] = f
            break
    for f in fn_textgrids:
        if filename_to_word(f) == word:
            d['textgrid_filename'] = f
            break
    return d

