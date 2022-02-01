Python: 

T2_estimate.py -> calculate T2 map from data with TR = 1000 ms and variing TE with linear fit -> get T2 map and S0
Signal_TE_dependence.py -> Calculate the expected signal in dependence of TE with the results from T2_estimate.py
SNR_TE_dependence.py -> calculate SNR(TE) with S(TE) and sigma-map 

all_toghether.py -> load niftis, take definitions from T2_estimate.py, Signal_TE_dependence.py and SNR_TE_dependence.py, do all the previous steps in one python fiel



Filenames: 

Files from /data/pt_02015/211021_Heschl_Bruker_Magdeburg/raw_nii 

ACQ_USER_PVMmcw_DWEpiWavev7X89P1.nii -> E89 TE = 40ms
ACQ_USER_PVMmcw_DWEpiWavev7X90P1.nii -> E90 TE = 50 ms
ACQ_USER_PVMmcw_DWEpiWavev7X91P1.nii -> E91 TE = 60 ms
ACQ_USER_PVMmcw_DWEpiWavev7X92P1.nii -> E92 TE = 70 ms
ACQ_USER_PVMmcw_DWEpiWavev7X93P1.nii -> E93 TE = 100 ms

Files from /data/pt_02015/211021_Heschl_Bruker_Magdeburg/nii_new

mask.nii
noise_sigmas.nii


Post mortem T2 times in literature: 

Roebrock 2020
Dawe 2009




