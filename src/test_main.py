import runpy
import pytest
import mne
from src import config
import os

def test_main_outputs():

    global globals_dict

    globals_dict = runpy.run_path('__main__.py')
 

    variables_to_test = ['subject_num', 'report', 'raw_info', 'epochs',
                         'epochs_combined', 'evoked', 'conditions', 'csd',
                         'csd_baseline', 'tfr_pres', 'tfr_food', 'psd']
    
    variable_expected_types = [str, mne.Report, mne.Info, mne.EpochsArray, mne.EpochsArray,  
                               mne.evoked.Evoked, list, mne.time_frequency.CrossSpectralDensity, 
                               mne.time_frequency.CrossSpectralDensity, mne.time_frequency.AverageTFR, 
                               mne.time_frequency.AverageTFR, mne.time_frequency.psd]

    assert all(var in globals_dict for var in variables_to_test)
    
    # Test that all variables are not None
    assert all(globals_dict[var] is not None for var in variables_to_test)

    # Test that all variables have correct data_types
    assert all(isinstance(globals_dict[var], variable_expected_types[i]) for i, var in enumerate(variables_to_test))
