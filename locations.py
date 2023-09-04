import glob

baldey = '../BALDEY/'
baldey_audio = baldey + 'recordings/'
fn_baldey_audio = glob.glob(baldey_audio + '*/*.wav')
baldey_textgrids = baldey + 'textgrids/'
fn_baldey_textgrids = glob.glob(baldey_textgrids + '*.TextGrid')
baldey_data_filename = baldey + 'baldey.txt'
baldey_column_filename = baldey + 'baldey_columns.txt'
baldey_wordset_filename = baldey + 'word_set.txt'

mald = '../MALD/'
mald_audio = mald + 'recordings/'
fn_mald_audio = glob.glob(mald_audio + '*/*.wav')
mald_textgrids = mald + 'textgrids/'
fn_mald_textgrids = glob.glob(mald_textgrids + '*/*.TextGrid')
mald_word_data_filename = mald + 'MALD1_ItemData.txt'
mald_response_data_filename = mald + 'ResponseData.txt'
mald_subject_data_filename = mald + 'MALD1_SubjectData.txt'
mald_wordset_filename = mald + 'word_set.txt'
