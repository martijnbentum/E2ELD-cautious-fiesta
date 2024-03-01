import codevectors
import codevectors_lda as clda
import json
import locations
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle
from progressbar import progressbar
import word

mald_vowels = 'ʊ i ai ʌ ɪ ɔ ɛ ɑ aʊ oʊ u ɔɪ eɪ ɝ æ'.split(' ')

def _make_mald_vowels_index_dict(all_mald_vowels = None,frames = None, 
        w = None):
    if not all_mald_vowels:
        if not frames: frames = clda.get_frames(w = w).frames
        vowel_indices = clda.load_vowel_frame_indices()
        f = [frames[i] for i in vowel_indices]
        all_mald_vowels = [frame.phoneme.ipa for frame in f]
    d = {}
    for i,v in enumerate(all_mald_vowels):
        if v not in d.keys(): d[v] = []
        d[v].append(i)
    with open('../mald_vowels_dataset_indices_dict.json', 'w') as f:
        json.dump(d, f)
    return d

def load_mald_vowel_specific_dataset_indices():
    with open('../mald_vowels_dataset_indices_dict.json', 'r') as f:
        d = json.load(f)
    return d

def make_index_mapper():
    '''map vowel specific index to index in codevector dataset'''
    vowel_indices = clda.load_vowel_frame_indices()
    frame_index_to_dataset_index = {}
    dataset_index_to_frame_index = {}
    for i,frame_index in enumerate(vowel_indices):
        frame_index_to_dataset_index[frame_index] = i
        dataset_index_to_frame_index[i] = frame_index
    return frame_index_to_dataset_index, dataset_index_to_frame_index

def load_vowel_dataset():
    X, y = clda.load_dataset(only_vowels = True)
    return X, y

def make_leave_one_out_train_test_sets(dataset= None, leave_out_vowel = 'ɛ'):
    '''make leave one out train test sets'''
    if not dataset: dataset = load_vowel_dataset()
    X,y = dataset

    vowel_specific_dataset_indices=load_mald_vowel_specific_dataset_indices()
    leave_out_dataset_indices=vowel_specific_dataset_indices[leave_out_vowel]

    train_indices = [i for i in range(len(X)) if i not in 
        leave_out_dataset_indices]
    print('make dataset')
    X_train = X[train_indices]
    y_train = y[train_indices]
    X_test = X[leave_out_dataset_indices]
    y_test = y[leave_out_dataset_indices]

    return X_train, X_test, y_train, y_test

def _make_clf_filename(leave_out_vowel):
    filename = locations.leave_one_out_codevectors_lda 
    filename += 'clf_' + leave_out_vowel + '.pickle'
    return filename

def train_all_lda(dataset = None):
    if not dataset: dataset = load_vowel_dataset()
    X, y = dataset
    for leave_out_vowel in mald_vowels:
        print('training', leave_out_vowel)
        filename = _make_clf_filename(leave_out_vowel)
        if os.path.exists(filename): continue
        train_lda(X, y, leave_out_vowel = leave_out_vowel, save = True)
        

def train_lda(X, y, leave_out_vowel = 'ɛ', save = False):
    '''train an LDA based on the vowel spectral balance datase 
    use make_dataset function to create the dataset (X, y)
    '''
    dataset = X,y
    X_train, X_test, y_train, y_test = make_leave_one_out_train_test_sets(
        dataset, leave_out_vowel = leave_out_vowel)
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    cr = classification_report(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    report = {'classification_report': cr, 'mcc': mcc}
    data = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train,
        'y_test': y_test}
    if save:
        filename = _make_clf_filename(leave_out_vowel)
        with open(filename, 'wb') as f:
            pickle.dump(clf, f)
        report_filename = locations.leave_one_out_codevectors_lda 
        report_filename += 'report_' + leave_out_vowel + '.json'
        with open(report_filename, 'w') as f:
            json.dump(report, f)
    return clf, data, report

