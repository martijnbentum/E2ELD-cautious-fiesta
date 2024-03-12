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

def handle_audio_filename(filename):
    d = {}
    name = filename.split('/')[-1].split('.')[0]
    d['name'] = name
    d['number'], d['word'] = _get_number_word(name)
    d['stress_pattern'] = name.split('_')[1]
    sc = 'sentence' if name.split('_')[2] == 'sent' else 'isolation'
    d['speech_condition'] = sc
    d['repetition'] = int(name.split('_')[3].replace('rep', ''))
    return d

def _make_coolest_audio_info():
    audio_info = {}
    for filename in locations.fn_coolest_audio:
        audio_info[filename] = sox.audio_info(filename)
    with open(locations.coolest + 'audio_info.json', 'w') as f:
        json.dump(audio_info, f, indent=4)
    return audio_info

def load_coolest_audio_info():
    with open(locations.coolest + 'audio_info.json', 'r') as f:
        audio_info = json.load(f)
    return audio_info
