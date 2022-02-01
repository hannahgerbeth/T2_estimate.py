import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import time
from T2_estimate import T2_map_calc
from Signal_TE_dependence import S_TE
from SNR_TE_dependence import Sig2Noise_TE

""" Get Data from nifit (nii)-Files """
# load mask nifti "mask_filename"
mask_img = nib.load('mask.nii') # [80, 50, 120]
temp_mask = mask_img.get_fdata().astype(np.bool)  # change type to boolean
mask = np.transpose(temp_mask, (2, 0, 1))  # change mask shape from [80, 50, 120] to [120, 80, 50]

# load sigma-map (calculated from noisemap) nifti "filename"
sigmamap_img = nib.load('noise_sigmas.nii')
temp_sigma_map = sigmamap_img.get_fdata()
sigma_map = np.transpose(temp_sigma_map, (2, 0, 1))  # change sigma-map shape from [80, 50, 120] to [120, 80, 50]
affine = sigmamap_img.affine

# load data nifti "data_filename" with nibabel
data_img_89 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X89P1.nii')
data_89 = data_img_89.get_fdata()
affine = data_img_89.affine
# transpose data to make it align with mask
data_89_TE_40 = np.flip(np.transpose(data_89, (1, 0, 2)), axis=(2, 0))  # change data shape from [80, 120, 50] to [120, 80, 50]

data_img_90 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X90P1.nii')
data_90 = data_img_90.get_fdata()
affine = data_img_90.affine
data_90_TE_50 = np.flip(np.transpose(data_90, (1, 0, 2)), axis=(2, 0))

data_img_91 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X91P1.nii')
data_91 = data_img_91.get_fdata()
affine = data_img_91.affine
data_91_TE_60 = np.flip(np.transpose(data_91, (1, 0, 2)), axis=(2, 0))

data_img_92 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X92P1.nii')
data_92 = data_img_92.get_fdata()
affine = data_img_92.affine
data_92_TE_70 = np.flip(np.transpose(data_92, (1, 0, 2)), axis=(2, 0))

data_img_93 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X93P1.nii')
data_93 = data_img_93.get_fdata()
affine = data_img_93.affine
data_93_TE_100 = np.flip(np.transpose(data_93, (1, 0, 2)), axis=(2, 0))


""" T2 map estimation """
# echo times in ms
TE_time = np.array([40, 50, 60, 70, 100])
# data_array arranged in shape (80, 50, 120, 5)
data_decay = np.transpose(np.array([data_89_TE_40, data_90_TE_50, data_91_TE_60, data_92_TE_70, data_93_TE_100]),
                          (1, 2, 3, 0))


T2_map, S0_fit = T2_map_calc(mask, data_decay, TE_time, range=None) # shape of T2_map and S0: [120, 80, 50]
T2_map_fixed_range = T2_map_calc(mask, data_decay, TE_time, range=(0, 250))[0]


""" Calculate signal in dependence of TE """
wf_dur = np.arange(12, 22, 0.5) # planar waveform durations

# parameters of the last measurement
TE_min = 40 #ms
dur = 12.5 #ms
spacing = 5 #ms
t_total = dur + spacing + dur

t_epi_div2 = TE_min - t_total # t_total + T_epi/2 = TE, T_epi/2 represents a factor in ms

# partameters for new waveforms
TE_list = [] # TE for the new waveforms in ms

for i in range(len(wf_dur)):
    space = 4.5 # ms
    t_total_wf = wf_dur[i] + space + wf_dur[i]
    TE_list.append(t_total_wf + t_epi_div2)

Sig_TE = S_TE(TE_list, T2_map, S0_fit, mask)  # shape of Sig_TE = [120, 80, 50, 20]


""" Sanity Check: SNR estimation for the waveform that was used in the latest measurement"""
# take a S(b0) from a previous scan, e.g. ACQ_USER_PVMmcw_DWEpiWavev7X89P1.nii (S_TE[0]) with TE=40ms, TR=1000ms
# calculate S(b0)/sigma = SNR

snr_previous = Sig_TE[:, :, :, 0] / sigma_map  # shape [120, 80, 50]


""" Calculation of SNR map in dependence of TE"""
snr_TE = Sig2Noise_TE(Sig_TE, sigma_map)  # shape [120, 80, 50, 20]

plt.plot(TE_list, snr_TE[60, 40, 25, :], label='SNR(TE) of the voxel [60, 40, 25]')
plt.xlabel('Echo times [ms]')
plt.ylabel('SNR')
plt.plot(TE_list[0], snr_previous[60, 40, 25], 'ro', label='SNR of previous scan \n voxel [60, 40, 25] = {}'.format(snr_previous[60, 40, 25]))
plt.legend()
plt.title('FOV = [120, 80, 50], Voxel in the middle = [60, 40, 25]')
plt.show()

