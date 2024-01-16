import codevectors
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import os
from progressbar import progressbar
import word

def get_frames(w = None):
    if not w: w = word.get_frames()
    return codevectors.Frames(w)

def check_frames_ok(frames = None, save = False):
    if not frames: frames = get_frames(w = w).frames
    indices = []
    print('checking frames for ok, returing ok indices')
    for index, frame in enumerate(progressbar(frames)):
        if not hasattr(frame, 'phoneme'): continue 
        if not frame.phoneme: continue
        indices.append(index)
    if save:
        np.save('../MALD/frame_ok_indices.npy', indices)
    return indices

def load_frames_ok_indices(frames = None):
    if not os.path.exists('../MALD/frame_ok_indices.npy'):
        return check_frames_ok(frames = frames, save = True)
    return np.load('../MALD/frame_ok_indices.npy')

def make_dataset(frames = None, w = None, 
    save = False):
    '''convert codevector frames to numpy arrays
    for LDA training.
    '''
    if not frames: frames = get_frames(w = w).frames
    indices = load_frames_ok_indices(frames)
    codevector_size = frames[0].codevector.shape[0]
    X = np.zeros((len(indices), codevector_size))
    y = np.zeros((len(indices), 1), dtype = np.int8)
    print('making codevector dataset')
    for index in progressbar(indices):
        frame = frames[index]
        X[index] = frame.codevector
        y[index] = int(frame.phoneme.stressed)
    if save:
        np.savez('../MALD/codevectors.npz', X = X, y = y)
    return X, y

def load_dataset():
    '''load codevector dataset from disk'''
    if not os.path.exists('../MALD/codevectors.npz'):
        return make_dataset(save = True)
    data = np.load('../MALD/codevectors.npz')
    return data['X'], data['y']


