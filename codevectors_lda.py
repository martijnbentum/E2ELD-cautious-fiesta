import codevectors
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import word

def get_frames(w = None):
    if not w: w = word.get_frames()
    return codevectors.Frames(w)

def make_dataset(frames = None, w = None):
    '''convert codevector frames to numpy arrays
    for LDA training.
    '''
    if not frames: frames = get_frames(w = w).frames
    frame = frames[0]
    X = np.zeros((len(frames), len(frame.codevector)))
    y = np.zeros((len(frames), 1))
    for index, frame in enumerate(frames):
        X[index] = frame.codevector
        y[index] = int(frame.phoneme.stressed)
    return X, y
