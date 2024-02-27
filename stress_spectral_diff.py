import frequency_band
from matplotlib import pyplot as plt

def add_lda_score_to_spectral_tilt_json():
    d = frequency_band.load_spectral_tilt_json()
    X,y = frequency_band.make_dataset()
    clf, _ = frequency_band.train_lda(X, y, report = False)
    tf = clf.transform(X)
    for line, ld1_score in zip(d[1:], tf):
        line.append(round(ld1_score[0],3))
    d[0].append('lda_score')
    return d

def combine_multisyllable_word_lines(d = None):
    if not d: d = add_lda_score_to_spectral_tilt_json()
    output = {}
    for line in d[1:]:
        word = line[0]
        if word not in output.keys(): output[word] = [line]
        else: output[word].append(line)
    # select only words with more than 1 syllable
    output = {word:line for word,line in output.items() if len(line) > 1}
    return output

def _find_stressed_unstressed(lines):
    stressed = [line for line in lines if line[4]]
    unstressed = [line for line in lines if not line[4]]
    if len(stressed) != 1: return None, None
    stressed = stressed[0]
    return stressed, unstressed

def compute_lda_score_difference(d = None, multiple = False):
    if not d: d = combine_multisyllable_word_lines(d)
    output = []
    for word, lines in d.items():
        stressed, unstressed = _find_stressed_unstressed(lines)
        if not stressed or not unstressed: continue
        if not multiple:
            lda_diff = stressed[-1] - np.mean([x[-1] for x in unstressed])
            output.append(lda_diff)
        else:
            lda_diff = [stressed[-1] - x[-1] for x in unstressed]
            output.extend(lda_diff)
    return output

def plot_lda_score_difference(multiple = False):
    plt.ion()
    plt.figure()
    lda_diff = compute_lda_score_difference(multiple = multiple)
    plt.hist(lda_diff, bins = 50, color = 'black')
    plt.grid(alpha=0.3)
    plt.xlabel('LDA score difference')
    plt.ylabel('Counts')
    plt.show()

def plot_lda_hist(dataset = None, add_legend = True, minimal_frame = False,
        add_left = True, ylim = None, new_figure = True):
    if not dataset: dataset = frequency_band.make_dataset()
    X,y = dataset
    plt.ion()
    if new_figure: plt.figure()
    ax = plt.gca()
    if minimal_frame:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    clf, _ = frequency_band.train_lda(X, y, report = False)
    tf = clf.transform(X)
    if ylim: plt.ylim(ylim)
    plt.xlim(-4.5,2.8)
    plt.hist(tf[y==1], bins = 50, alpha=1, color = 'black', 
        label = 'stress')
    plt.hist(tf[y==0], bins = 50, alpha=0.7, color = 'orange', 
        label = 'no stress')
    plt.grid(alpha=0.3)
    if add_legend: plt.legend()
    if add_left: plt.ylabel('Counts')
    else:
        ax.spines['left'].set_visible(False)
        ax.tick_params(left = False)
        ax.set_yticklabels([])
    plt.xlabel('Spectral (LD1)')
    plt.show()
