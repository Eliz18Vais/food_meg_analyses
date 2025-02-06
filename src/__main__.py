"""

Itterate over all subjects folders, convert mat files of epoched data to EpochsArray instances, combine epochs
to the desired conditions and save the two epochs arrays to fif files.
Analyse epochs_combined data using CSD, TFR, GFP, PSD and topo plots. 

Subjects foldes must contain only one mat file that contains the epoched data and one raw MEG bti recording.

"""
"""importations of libraries"""

if __name__ == "__main__":

    from typeguard import install_import_hook
    
    install_import_hook()

    import numpy as np
    import numbers
    import os
    import mne
    import glob
    import warnings
    from mne.time_frequency import csd_morlet, read_spectrum, read_csd, read_tfrs
    import traceback
    from pymatreader import read_mat
    from src import config
    from mat_to_epochs_conversion import convert_main_funcs, combine_epochs, create_info # using * didn't work for some reason
    from analyses import *
    import sys
    import add_to_report
    from tests import output_tests

    package_path = "C:/Projects/food_meg_analyses" 
    
    if package_path not in sys.path:
        sys.path.insert(0, package_path)
   

    # in case one of the modules is not installed or can not be found by python using the system variables:
    # except Exception as e:
    #     print("An error occured:", e)
    #     traceback.print_exc()

    try:

        directory = config.subject_directory_pattern # directory pattern for itterating over subject folders

        # itterate over all subjects folders
        for folder in glob.iglob(directory): 

            if os.path.exists(folder): # the subject folder that contains the mat file with epoched data and the raw MEG recordings per subject

                try:  

                    subject_num = folder.split("SUBS_DIR\\", 1)[1]


                    os.chdir(folder)

                    raw_info = create_info.extract_raw_info(folder)
                    output_tests.test_raw_info(raw_info)

                    
                    # recieves a file path to the mat file, glob.glob returns a list of all paths found with the pattern.
                    # [0] for returning the first and only element in the list.
                    epochs, evoked = convert_main_funcs.convert_mat_to_epochs(glob.glob(config.mat_file_path_pattern)[0], info=raw_info) 
                    
                    # combine epochs by new conditions (new_event_ids):
                    epochs_combined = combine_epochs.combine_epochs(epochs, config.event_ids, config.new_event_ids)
                    output_tests.test_epochs_combined(epochs_combined)

                    # extract conditions for csd cmputation per condition:
                    conditions =  list(epochs_combined.event_id.keys())

                    # Suppress warning about wavelet length.

                    for condition in conditions:

                        # csd calculation post stimulus over the desired frequency range per condition, save and add to report
                        csd = compute_csd.compute_csd(epochs_combined, condition, config.freq_bands, config.post_stim_time) 
                        output_tests.test_csd(csd)

                    # csd calculation of baseline over the desired frequency range, save and add to report. (calculates csd baseline for the last 
                    # condition in loop, we assume that all conditions have same baseline activity)
                    csd_baseline = compute_csd.compute_csd(epochs, condition, config.freq_bands, config.baseline_time, is_base_line=True)
                    output_tests.test_csd(csd_baseline)
                    
                    # compute tfrs for desired contrast of conditions, over the frequencies in freqs and save:
                    tfr_pres = tfr_psd_analyses.compute_tfr_contrast(epochs=epochs, freqs=np.arange(8, 24, 2), con1=('pres_1', config.pres_1), 
                    con2=('pres_2', config.pres_2))
                    output_tests.test_tfr(tfr_pres)


                    tfr_food = tfr_psd_analyses.compute_tfr_contrast(epochs=epochs,  freqs=np.arange(8, 24, 2), con1=('food',config.food), 
                    con2=('nonfood',config.nonfood))

                    psd =  tfr_psd_analyses.compute_psd(evoked_instance=evoked, fmin=config.freq_bands[0][0], fmax=config.freq_bands[-1][-1], tmin=config.baseline_time[0], tmax=config.post_stim_time[1], picks='meg')
                    output_tests.test_psd(psd)

                    report = mne.Report(title=f"report for {subject_num}")

                    add_to_report.add_to_report(report, subject_num)

                except Exception as e:
                    print("An error occured:", e)
                    traceback.print_exc()


            else:
                raise FileNotFoundError

    except Exception as e:
        print("An error occured:", e)
        traceback.print_exc()
