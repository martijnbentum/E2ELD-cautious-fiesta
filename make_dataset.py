import itertools
import locations
import os

def make_mald_variable_stress_syllable(sd = None):
    d = locations.mald_variable_stress_syllable_directory
    os.makedirs(d,exist_ok=True)
    if not sd: _,sd = ds.stress_variability_mald(d,50,0.05,n_include=None)
    temp = [x['syllables'] for x in sd.values()]
    syls = list(itertools.chain(*temp))
    
