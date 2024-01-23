import codevectors
import codevectors_lda
import frequency_band
import json
from matplotlib import pyplot as plt
import numpy as np
from progressbar import progressbar
from sklearn.linear_model import LinearRegression
import stress_spectral_diff

def load_spectral_tilt_with_lda_score():
    return stress_spectral_diff.add_lda_score_to_spectral_tilt_json()

def xy_row_index_to_frame(row_index,frames,indices):
    return frames[indices[row_index]]

def frame_index_to_xy_row_index(frame_index,vowel_indices):
    index = np.where(vowel_indices == frame_index)[0][0]
    return index

def get_frame_lda_score(tf, frame_index, vowel_indices):
    index = frame_index_to_xy_row_index(frame_index, vowel_indices)
    return float(tf[index][0])

def word_to_spectral_tilt_lda_score_lines(word, d = None):
    if not d: d = load_spectral_tilt_with_lda_score()
    output = []
    for line in d:
        if line[0] == word:
            output.append(line)
    return output

def make_word_dict(frames = None, w = None):
    if not frames: frames = codevectors.Frames(words = w).frames
    vowel_indices = codevectors_lda.load_vowel_frame_indices()
    d = load_spectral_tilt_with_lda_score()
    output = {}
    for frame_index in progressbar(vowel_indices):
        frame = frames[frame_index]
        frame.frame_index = frame_index
        word = frame.name.lower()
        if word not in output.keys():
            output[word] = {}
            output[word]['frames'] = [frame]
            temp = word_to_spectral_tilt_lda_score_lines(word, d)
            output[word]['spectral_tilt'] = temp
        else:
            output[word]['frames'].append(frame)
    return output

def make_phoneme_list(word_dict = None, frames = None, w = None, save = False):
    if not word_dict: word_dict = make_word_dict(frames = frames, w = w)
    output = []
    for word, values in progressbar(word_dict.items()):
        spectral_tilt = values['spectral_tilt']
        for line in spectral_tilt:
            phoneme = line[3]
            stressed = line[4]
            phoneme_index = line[5]
            st_lda = line[-1]
        for frame in values['frames']:
            phoneme_index == frame.phoneme.phoneme_index
            frame_index = int(frame.frame_index)
            output.append([word, phoneme, stressed, phoneme_index, 
                st_lda, frame_index])
    phoneme_list = add_frame_lda_to_phoneme_list(output)
    if save: save_phoneme_list(phoneme_list)
    return output

def add_frame_lda_to_phoneme_list(phoneme_list):
    X,y = codevectors_lda.load_dataset(only_vowels = True)
    clf = codevectors_lda.load_lda(only_vowels = True)
    tf = clf.transform(X)
    vowel_indices = codevectors_lda.load_vowel_frame_indices()
    for line in progressbar(phoneme_list):
        frame_index = line[5]
        lda_score = get_frame_lda_score(tf, frame_index, vowel_indices)
        line.append(lda_score)
    return phoneme_list

def save_phoneme_list(phoneme_list= None, word_dict = None, frames = None):
    if not phoneme_list: phoneme_list= make_phoneme_list(word_dict = word_dict, 
            frames = frames)
    with open( '../MALD/phoneme_list.json', 'w') as filename:
        json.dump(phoneme_list, filename)    

def load_phoneme_list():
    with open( '../MALD/phoneme_list.json') as filename:
        phoneme_list= json.load(filename)
    return phoneme_list
        
def lm():
    pl = load_phoneme_list()
    iv_spectral_tilt = np.array([x[4] for x in pl]).reshape(len(pl),1)
    dv_codevector = np.array([x[-1] for x in pl])
    x_values = np.array([np.min(iv_spectral_tilt), np.max(iv_spectral_tilt)])
    print(x_values)
    lm = LinearRegression()
    lm.fit(iv_spectral_tilt, dv_codevector)
    print('intercept',lm.intercept_)
    print('slope',lm.coef_)
    print('r²',lm.score(iv_spectral_tilt, dv_codevector))
    y_values = lm.coef_ * x_values + lm.intercept_
    print(x_values,y_values)
    plt.ion()
    plt.figure()
    plt.scatter(iv_spectral_tilt, dv_codevector, alpha = 0.01,color = 'blue')
    plt.plot(x_values,y_values, color = 'black')
    plt.xlabel('LDA score spectral tilt')
    plt.ylabel('LDA score codevector')
    plt.show()


