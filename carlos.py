import frequency_band as fb
import glob
import os
import progressbar

directory = '/Users/martijn.bentum/Downloads/AllSpeakers/'

fn = glob.glob(directory + '*.wav')


def handle_filename(s):
    return directory + s+'.wav'

def format_line(line):
    o = {}
    try:
        o['filename'] = handle_filename(line[0])
        o['n'] = int(line[1])
        o['start'] = float(line[2])
        o['end'] = float(line[3])
        o['f1'] = list(map(int,line[4].split('-')))
        o['f2'] = list(map(int,line[5].split('-')))
        o['f3'] = list(map(int,line[6].split('-')))
    except ValueError: return None
    return o

def handle_line(line):
    '''compute the power in frequency bands and convert to decibels
    for a specific vowel in a word.
    '''
    signal, sr = fb.load_audio_file(line['filename'], start=line['start'], 
        end=line['end'], sample_rate = 48_000)
    frequencies, power_spectrum = fb.compute_power_spectrum(signal)
    fb1 = fb.frequency_band_to_db(*line['f1'], frequencies, power_spectrum)
    fb2 = fb.frequency_band_to_db(*line['f2'], frequencies, power_spectrum)
    fb3 = fb.frequency_band_to_db(*line['f3'], frequencies, power_spectrum)
    if sum([x < 0 for x in [fb1,fb2,fb3]]) > 0: return None
    line['fb1'] = fb1
    line['fb2'] = fb2
    line['fb3'] = fb3
    return line

def format_list():
    output, error = [], []
    l = open(directory + 'list1.txt', 'r').read().split('\n')
    l = [x.split('\t') for x in l if x]
    for x in l:
        if not x: continue
        line = format_line(x)
        if line: output.append(line)
        else: error.append(x)
    return output, error

def handle_list():
    l, format_error = format_list()
    output, fb_error, file_error = [], [], []
    for line in progressbar.progressbar(l):
        if not os.path.isfile(line['filename']): 
            file_error.append(line)
            continue
        line = handle_line(line)
        if not line: fb_error.append(line)
        else: output.append(line)
    return output, format_error, fb_error, file_error

def line_dict_to_list(line):
    o = [line['filename'].split('/')[-1], line['n'], 
        line['start'], line['end'],
        line['fb1'], line['fb2'], line['fb3']]
    return list(map(str,o))


#def frequency_band_to_db(freq_lower_bound, freq_upper_band, frequencies, 
    
