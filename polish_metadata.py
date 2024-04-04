import locations

def load_clip_durations():
    with open(locations.cv_polish + 'clip_durations.tsv') as f:
        clip_durations = f.read().split('\n')
    durations = {}
    for line in clip_durations[1:]:
        if not line: continue
        filename, duration = line.split('\t')
        durations[filename] = int(duration)
    return durations
