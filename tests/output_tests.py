
import mne
from src import config

def test_subject_num(subject_num: str):
    import fnmatch
    assert fnmatch.fnmatch(subject_num, "subject_*")

def test_raw_info(raw_info: mne.Info):
    assert 'loc' in raw_info

def test_epochs_combined(epochs_combined: mne.EpochsArray):   
    assert epochs_combined.event_id.keys() == config.new_event_ids.keys()


def test_csd(csd: mne.time_frequency.CrossSpectralDensity):
    assert csd.n_channels == config.channels_number

def test_tfr(tfr: mne.time_frequency.AverageTFR):
    assert tfr.get_data().shape == (config.channels_number, config.time_points)

    
def test_psd(psd: mne.time_frequency.Spectrum):
    assert len(psd.ch_names) == config.channels_number

output_test = {'subject_num': test_subject_num, 'raw_info': test_raw_info, 'epochs_combined': test_epochs_combined,
                'csd': test_csd, 'tfr': test_tfr,'psd': test_psd}
    
    


