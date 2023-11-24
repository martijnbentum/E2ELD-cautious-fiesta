import glob

baldey = '../BALDEY/'
baldey_audio = baldey + 'recordings/'
fn_baldey_audio = glob.glob(baldey_audio + '*/*.wav')
baldey_textgrids = baldey + 'textgrids/'
fn_baldey_textgrids = glob.glob(baldey_textgrids + '*.TextGrid')
baldey_tables_directory = baldey + 'tables/'
baldey_data_filename = baldey + 'baldey.txt'
baldey_column_filename = baldey + 'baldey_columns.txt'
baldey_wordset_filename = baldey + 'word_set.txt'

mald = '../MALD/'
mald_audio = mald + 'recordings/'
fn_mald_audio = glob.glob(mald_audio + '*/*.wav')
mald_word_recordings = mald_audio + 'words/'
mald_word_16khz_recordings = mald_audio + 'words_16khz/'
mald_textgrids = mald + 'textgrids/'
fn_mald_textgrids = glob.glob(mald_textgrids + '*/*.TextGrid')
mald_word_data_filename = mald + 'MALD1_ItemData.txt'
mald_response_data_filename = mald + 'ResponseData.txt'
mald_subject_data_filename = mald + 'MALD1_SubjectData.txt'
mald_wordset_filename = mald + 'word_set.txt'
mald_table_directory = mald + 'tables/'
mald_prosodic_syllables_directory = mald + 'prosodic_syllables/'

mald_codevector_indices = mald + 'codevector_indices/'  
codebook_filename = mald_codevector_indices + 'codebook.npy'

mald_variable_stress_syllable_directory = mald + 'variable_stress_syllable/'

word_to_filenames_dict = '../word_to_filenames_dict.json'

celex_directory = '../CELEX/'
celex_english_phonology_file = celex_directory+ 'EPW.CD'
celex_dutch_phonology_file = celex_directory + 'DPW.CD'
