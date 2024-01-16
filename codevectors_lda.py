import codevectors
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import word

def get_frames(w = None):
    if not w: w = word.get_frames()
    return codevectors.Frames(w)

def count_ok_frames(frames):
    indices = []
    for index, frame in enumerate(frames):
        if not hasattr(frame, 'phoneme') 
        if not frame.phoneme: continue
        if not hasattr(frame.codevector): continue
        if not hasattr(frame.codevector.shape): continue
        if not frame.codevector.shape[0] == codevector_size: continue
        indices.append(index)
    return indices

def make_dataset(frames = None, w = None, save = False):
    '''convert codevector frames to numpy arrays
    for LDA training.
    '''
    if not frames: frames = get_frames(w = w).frames
    frame = frames[0]
    codevector_size = frame.codevector.shape[0]
    indices = count_ok_frames(frames)
    X = np.zeros((len(indices), codevector_size))
    y = np.zeros((len(indices), 1))
    for index in indices:
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


