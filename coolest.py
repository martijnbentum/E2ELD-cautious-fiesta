import json
import locations
import sox

def _get_number_word(name):
    for i,char in enumerate(name):
        if not char.isdigit():
            break
    number = name[:i]
    word = name[i:]
    return number, word.split('_')[0]

def _add_prompt_info(d, prompts):
    name = d['name'].replace(d['number'],'')
    d['trial'],d['prompt'] = None, None
    for line in prompts:
        if line[1] == name:
            d['trial'] = int(line[0])
            d['prompt'] = line[2]
            break

def handle_audio_filename(filename, audio_info = None, prompts = None):
    d = {}
    name = filename.split('/')[-1].split('.')[0]
    d['name'] = name
    d['number'], d['word'] = _get_number_word(name)
    d['stress_pattern'] = name.split('_')[1]
    sc = 'sentence' if name.split('_')[2] == 'sent' else 'isolation'
    d['speech_condition'] = sc
    d['repetition'] = int(name.split('_')[3].replace('rep', ''))
    if audio_info: d.update(audio_info[filename])
    if prompts: _add_prompt_info(d, prompts)
    return d

def filename_to_word(filename):
    return handle_audio_filename(filename)['word']

def filename_to_name(filename):
    return handle_audio_filename(filename)['name']

def filename_to_name(filename):
    return handle_audio_filename(filename)['number']

def get_textgrid_table_filename(filename):
    textgrid_filename = filename.replace('Recordings','textgrids')
    textgrid_filename = textgrid_filename.replace('.wav','_cor.TextGrid')
    table_filename = locations.coolest_tables + filename.split('/')[-1]
    table_filename = table_filename.replace('.wav','_cor.csv')
    return textgrid_filename, table_filename

def get_word_line_in_table(table, word):
    word_line, word_maus = None, None
    for line in table:
        if line[1] == 'Word':
            word_line = line
        if line[1] == 'ORT-MAU': 
            if line[2] == word: word_maus= line
            if word == 'komeet' and line[2] == 'comeet':word_maus= line
    return word_line, word_maus

def _make_audio_info():
    audio_info = {}
    for filename in locations.fn_coolest_audio:
        audio_info[filename] = sox.audio_info(filename)
    with open(locations.coolest + 'audio_info.json', 'w') as f:
        json.dump(audio_info, f, indent=4)
    return audio_info

def load_audio_info():
    with open(locations.coolest + 'audio_info.json', 'r') as f:
        audio_info = json.load(f)
    return audio_info

def load_prompts():
    with open(locations.coolest_prompts_filename, 'r') as f:
        prompts = f.read().split('\n')
    header = prompts[0].split(',')
    temp= [x.split(',') for x in prompts[1:] if x]
    data = []
    for line in temp:
        data.append([line[0],line[1],'. '.join([x.strip().strip('" ') 
            for x in line[2:]])])
    return header, data

def _make_word_data_header():
    audio_filenames = locations.fn_coolest_audio
    header, prompts = load_prompts()
    audio_info = load_audio_info()
    output = []
    for f in audio_filenames:
        d = handle_audio_filename(f,audio_info, prompts)
        output.append(d.values())
    with open(locations.coolest_word_data_filename, 'w') as f:
        f.write('\n'.join(['\t'.join(map(str,line)) for line in output]))
    with open(locations.coolest_word_header_filename, 'w') as f:
        f.write('\t'.join(d.keys()))

def load_word_data():
    with open(locations.coolest_word_data_filename, 'r') as f:
        data = [line.split('\t') for line in f.read().split('\n') if line]
    return data

def load_word_header():
    with open(locations.coolest_word_header_filename, 'r') as f:
        header = f.read().split('\t')
    return header
