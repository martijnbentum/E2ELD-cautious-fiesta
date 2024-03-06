import codevector_leave_one_out as clou
import json
import general
from matplotlib import pyplot as plt
import mccs
import numpy as np
import perceptron_leave_one_out as plou

def _results_to_mcc_list(results):
    return [x['mcc'] for x in results.values()]

def load_mccs():
    '''load the results for codevectors (c) and perceptrons (p) 
    load the leave one vowel in (i) and leave one vowel out (o) results
    get the mccs for each vowel of the four cases
    return the mccs
    '''
    temp = mccs.load_mccs(True)
    ci = _results_to_mcc_list( clou.get_results(True) )
    co = _results_to_mcc_list( clou.get_results(False) )
    ca = temp['Codevector']
    pi = _results_to_mcc_list( plou.get_results(True)['18'] )
    po = _results_to_mcc_list( plou.get_results(False)['18'] )
    pa = temp[18] 
    d = {'cv (in)':ci, 'cv (out)':co, 'cv (all)':ca,
        '18 (in)':pi, '18 (out)':po, '18 (all)':pa}
    return d

def plot_mccs(new_figure=True):
    plt.ion()
    if new_figure:plt.figure()
    plt.ylim(0,1)
    results = load_mccs()
    stats = general.compute_mccs_stats(results)
    x = range(len(results))
    means = [stats[key]['mean'] for key in stats]
    cis = [stats[key]['ci'] for key in stats]
    plt.errorbar(x, means, yerr=cis, fmt=',', markersize = 12, 
        color = 'black',elinewidth = 2.5, capsize = 9, capthick = 2.5)
    plt.grid(alpha=0.3)
    plt.xticks(range(len(results)), results.keys(), rotation=0)
    plt.ylabel("matthew's correlation coefficient")
    



