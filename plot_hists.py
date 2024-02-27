from matplotlib import pyplot as plt
import stress_intensity_diff as sid
import stress_pitch_diff as spd
import stress_duration_diff as sdd
import stress_spectral_diff as ssd
import frequency_band as fb
import formants

def plot_hists(intensities = None, pitch = None, durations = None, 
        lda_dataset = None, formant_data = None, w = None, ylim = (0,6500)) :
    if not intensities: intensities = sid.get_intensity_from_vowels(w)
    if not pitch: pitch = spd.load_pitch_json()
    if not durations: durations = sdd.get_durations_from_vowels(w = w)
    if not lda_dataset: lda_dataset = fb.make_dataset()
    if not formant_data: 
        formant_data = formants.compute_distance_to_global_mean(w)
    plt.ion()
    plt.figure()
    plt.subplot(1,5,1)
    sid.plot_stress_no_stress_distributions(intensities, new_figure = False, 
        add_legend = False, ylim = ylim, minimal_frame = True)
    plt.subplot(1,5,2)
    sdd.plot_stress_no_stress_distributions(durations, new_figure = False, 
        add_legend = False, ylim = ylim, minimal_frame = True, add_left = False)
    plt.subplot(1,5,3)
    formants.plot_stress_no_stress(formant_data, new_figure = False, 
        add_legend = False,ylim = ylim, add_left = False, minimal_frame = True)
    plt.subplot(1,5,4)
    spd.plot_hist_all_vowels(pitch, new_figure = False, add_legend = False,
        ylim = ylim, add_left = False, minimal_frame = True)
    plt.subplot(1,5,5)
    ssd.plot_lda_hist(lda_dataset, new_figure = False, add_legend = True, 
        minimal_frame = True, ylim = ylim, add_left = False)
