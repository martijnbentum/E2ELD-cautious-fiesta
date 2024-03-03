'''
module to plot perceptron leave one in vs leave one out results
code to compute the results can be found here:
https://github.com/martijnbentum/CGN_AUDIO_EXTRACT/blob/master/ld/perceptron_leave_one_out.py
'''
import codevector_leave_one_out
import json
import glob
import locations
from matplotlib import pyplot as plt

def get_results(leave_one_in = False):
    if leave_one_in:
        fn = glob.glob(locations.leave_one_in_perceptron + '*.json')
    else:
        fn= glob.glob(locations.leave_one_out_perceptron + '*.json')
    results = {}
    for f in fn:
        with open(f, 'r') as fin:
            d = json.load(fin)
        vowel = f.split('_')[-1].split('.')[0]
        layer = f.split('_')[-2]
        if layer not in results.keys():
            results[layer] = {}
        results[layer][vowel] = d
    return results

def plot_results(layer = '18', new_figure = True, color = 'black'):
    rloi = get_results()[layer]
    rli = get_results(leave_one_in = True)[layer]
    mccout = [v['mcc'] for k,v in rloi.items()]
    mccin = [v['mcc'] for k,v in rli.items()]
    if new_figure:plt.figure()
    plt.scatter(mccout, mccin, marker = '.', color = color)
    [plt.text(mccout[i]-0.003, mccin[i]+0.005, k, fontsize=12,color=color) 
        for i,k in enumerate(rloi.keys())]
    plt.xlabel('MCC leave one out')
    plt.ylabel('MCC leave one in')
    plt.grid(alpha = 0.3)
    plt.show()

def plot_perceptron_and_codevector_results():
    codevector_leave_one_out.plot_results(add_counts = False)
    plot_results(new_figure = False, color = 'blue')
    plt.ylim(0.18,0.92)
    plt.xlim(0.18,0.92)
    plt.show()
