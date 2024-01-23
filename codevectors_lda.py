import codevectors
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

def find_vowel_frame_indices(frames = None, save = False):
    if not frames: frames = get_frames(w = w).frames
    indices = []
    print('finding vowel frame indices')
    for index, frame in enumerate(progressbar(frames)):
        if not hasattr(frame, 'phoneme'): continue 
        if not frame.phoneme: continue
        if not hasattr(frame.phoneme, 'phoneme_type'): continue
        if frame.phoneme.phoneme_type =='vowel': 
            indices.append(index)
    if save:
        np.save('../MALD/vowel_frame_indices.npy', indices)
    return indices

def load_frames_ok_indices(frames = None):
    if not os.path.exists('../MALD/frame_ok_indices.npy'):
        return check_frames_ok(frames = frames, save = True)
    return np.load('../MALD/frame_ok_indices.npy')

def load_vowel_frame_indices(frames = None):
    if not os.path.exists('../MALD/vowel_frame_indices.npy'):
        return find_vowel_frame_indices(frames = frames, save = True)
    return np.load('../MALD/vowel_frame_indices.npy')

def make_dataset(frames = None, w = None, 
    save = False, only_vowels = False):
    '''convert codevector frames to numpy arrays
    for LDA training.
    '''
    if not frames: frames = get_frames(w = w).frames
    if only_vowels:indices = load_vowel_frame_indices(frames)
    else:indices = load_frames_ok_indices(frames)
    codevector_size = frames[0].codevector.shape[0]
    X = np.zeros((len(indices), codevector_size))
    y = np.zeros((len(indices), 1), dtype = np.int8)
    print('making codevector dataset')
    for i,frame_index in enumerate(progressbar(indices)):
        frame = frames[frame_index]
        X[i] = frame.codevector
        y[i] = int(frame.phoneme.stressed)
    if save and only_vowels:
        np.savez('../MALD/codevectors_vowels.npz', X = X, y = y)
    elif save:
        np.savez('../MALD/codevectors.npz', X = X, y = y)
    return X, y

def load_dataset(only_vowels = False):
    '''load codevector dataset from disk'''
    if only_vowels:
        if not os.path.exists('../MALD/codevectors_vowels.npz'):
            return make_dataset(save = True, only_vowels = True)
        data = np.load('../MALD/codevectors_vowels.npz')
        return data['X'], data['y']
    if not os.path.exists('../MALD/codevectors.npz'):
        return make_dataset(save = True)
    data = np.load('../MALD/codevectors.npz')
    return data['X'], data['y']

def train_lda(X, y, test_size = 0.33, report = True, save = True,
    only_vowels = False):
    '''train an LDA based on the vowel spectral balance datase 
    use make_dataset function to create the dataset (X, y)
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        X,y, test_size = test_size, random_state=42)
    clf = LinearDiscriminantAnalysis()
    clf.fit(X_train, y_train)
    if report:
        y_pred = clf.predict(X_test)
        print(classification_report(y_test, y_pred))
        print('MCC:', matthews_corrcoef(y_test, y_pred))
    data = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train,
        'y_test': y_test}
    if save:
        if only_vowels: filename = '../MALD/lda_vowels.pickle'
        else: filename = '../MALD/lda.pickle'
        with open(filename, 'wb') as f:
            pickle.dump(clf, f)
    return clf, data

def load_lda(only_vowels = False):
    '''load LDA from disk'''
    if only_vowels:
        with open('../MALD/lda_vowels.pickle', 'rb') as f:
            return pickle.load(f)
    with open('../MALD/lda.pickle', 'rb') as f:
        return pickle.load(f)

def plot_lda(X, y, clf = None, only_vowels = False):
    ''' fit an LDA based on data (X) and labels (y) and plot the results
    '''
    plt.ion()
    plt.clf()
    if not clf:clf = load_lda(only_vowels = only_vowels)
    tf = clf.transform(X)
    color = ['blue', 'red']
    labels = ['no stress', 'stress']
    for color, i, label in zip(color, [0,1], labels):
        if i == 0: marker = 'o'
        else: marker = 'x'
        n = len(tf[y==i])
        plt.scatter(tf[y==i], np.random.random(n), alpha=.01, color=color,
            label=label, marker = marker)
    legend = plt.legend()
    for lh in legend.legendHandles:
        lh.set_alpha(1)
    plt.xlabel('Linear Discriminant 1')
    plt.ylabel('Random jitter')
    plt.show()

def plot_lda_hist(X, y, clf = None):
    plt.ion()
    plt.figure()
    if not clf:clf = load_lda()
    tf = clf.transform(X)
    plt.hist(tf[y==0], bins = 50, alpha=0.7, color = 'blue', 
        label = 'unstressed')
    plt.hist(tf[y==1], bins = 50, alpha=0.7, color = 'red', 
        label = 'stressed')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xlabel('Linear Discriminant score')
    plt.ylabel('Counts')
    plt.show()



