import json
from matplotlib import pyplot as plt
import numpy as np
import general

spectral_balance_filename = '../mccs_density_lda_spectral_balance.json'
accoustic_correlates_filename='../mccs_density_clf_acoustic_correlates.json'
f1f1_filename = '../mccs_lda_f1f2.json'
combined_filename = '../mccs_combined_ac_lda_clf.json'
codevector_filename = '../mccs_lda_codevectors.json'
filenames = [spectral_balance_filename, accoustic_correlates_filename, 
    f1f1_filename, combined_filename, codevector_filename]


rename = {'intensity': 'Intensity', 'duration': 'Duration', 
    'formant': 'Formants', 'pitch': 'Pitch', 'spectral_balance': 'Spectral',
    'f1f2': 'F1-F2','combined': 'Combined', 'codevector': 'Codevector'}


def load_mccs(add_perceptron = False):
    temp, results= {}, {}
    for filename in filenames:
        with open(filename) as fin:
            d = json.load(fin)
        temp.update(d)
    for key,name in rename.items():
        results[name] = temp[key]
    if add_perceptron: results = _add_perceptron_w2v_probe_mccs(results)
    return results

def _add_perceptron_w2v_probe_mccs(results = None):
    if results is None: results = load_mccs()
    with open('../perceptron_all_word_results_layer_rs.json') as fin:
        d = json.load(fin)
    layers = ['cnn',1,6,12,18,21,24] 
    temp = {}
    for layer in layers:
        temp[layer] = []
        for k,v in d.items():
            l = k.split('-')[0]
            if str(layer) == l:
                temp[layer].append(v['mcc'])
    results.update(temp)
    return results
    
def plot_mccs(new_figure=True, add_perceptron = False):
    plt.ion()
    if new_figure:plt.figure()
    plt.ylim(0,1)
    results = load_mccs(add_perceptron = add_perceptron)
    stats = general.compute_mccs_stats(results)
    x = range(len(results))
    means = [stats[key]['mean'] for key in stats]
    cis = [stats[key]['ci'] for key in stats]
    plt.errorbar(x, means, yerr=cis, fmt=',', markersize = 12, 
        color = 'black',elinewidth = 2.5, capsize = 9, capthick = 2.5)
    plt.grid(alpha=0.3)
    plt.xticks(range(len(results)), results.keys(), rotation=45)
    plt.ylabel("matthew's correlation coefficient")
    # y = np.arange(0,1.1,.1)
    # plt.yticks(y, [str(round(i,2)) for i in y])






