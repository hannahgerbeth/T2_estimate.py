import numpy as np
import nibabel as nib
import time


# calculate S(TE)

def S_TE(TElist, T2map, S0_fit, mask):
    # TElist is a list with the TEs for different waveforms and waveform durations
    # T2 map, S0 (fit) and mask have data dimension [120, 80, 50]
    # return: S_TE = [read, phase, slice, time], where time = number of TEs
    # -> signal in dependence of different TEs, data for each TE is in the fourth dimension
    S_TE = np.zeros(T2map.shape[:3] + (len(TElist),))
    # print(S_TE.shape)

    for i in range(len(TElist)):
        for xyz in np.ndindex(T2map.shape[:3]):
            if mask[xyz]:
                S_TE[xyz][i] = S0_fit[xyz] * np.exp(- TElist[i] / T2map[xyz])
    return S_TE


"""------------------------------TEST-------------------------------------"""

if __name__ == '__main__':
    start_time = time.time()

    wf_dur = np.arange(12, 22, 0.5)  # waveform durations

    # parameters of the last measurement
    TE_min = 40  # ms
    dur = 12.5  # ms
    spacing = 5  # ms
    t_total = dur + spacing + dur

    t_epi_div2 = TE_min - t_total  # t_total + T_epi/2 = TE, T_epi/2 represents a factor in ms

    # print(t_epi_div2)

    # partameters for new waveforms
    TE_list = []  # TE for the new waveforms in ms

    for i in range(len(wf_dur)):
        space = 4.5  # ms
        t_total_wf = wf_dur[i] + space + wf_dur[i]
        TE_list.append(t_total_wf + t_epi_div2)

    print(TE_list)

    # load T2 map
    T2_img = nib.load('T2_map.nii')
    T2_map = T2_img.get_fdata()
    affine = T2_img.affine
    #print('T2', T2_map.shape)

    # load S0 from T2 fit
    S0_fit_img = nib.load('S0_fromT2fit.nii')
    S0_fitT2 = S0_fit_img.get_fdata()
    affine = S0_fit_img.affine
    #print('S0_fitT2', S0_fitT2.shape)

    # load mask nifti "mask_filename"
    mask_img = nib.load('mask.nii')
    temp_mask = mask_img.get_fdata().astype(np.bool)  # change type to boolean
    mask = np.transpose(temp_mask, (2, 0, 1))
    #print('mask', mask.shape)

    """
    # calculate S(TE)
    def S_TE(TElist, T2map, range=(0, 200)):
        S_TE = np.zeros((len(TElist),) + T2map.shape[:3])
        #print(S_TE.shape)
        if range:
            for i in range(len(TElist)):
                for xyz in np.ndindex(T2map.shape[:3]):
                    if mask[xyz]:
                        S_0 = 1
                        temp = S_0 * np.exp(- TElist[i]/ T2map[xyz])
                        if temp < range[0] or temp > range[1]:
                            S_TE[i][xyz] = 0
                        else:
                            S_TE[i][xyz] = temp
            return S_TE
        else:
            for i in range(len(TElist)):
                for xyz in np.ndindex(T2map.shape[:3]):
                    if mask[xyz]:
                        S_0 = 1
                        S_TE[i][xyz]= S_0 * np.exp(- TElist[i]/ T2map[xyz])
            return S_TE

    """

    Sig_TE = S_TE(TE_list, T2_map, S0_fitT2, mask)

    #print(Sig_TE.shape)
    #print(Sig_TE[:, :, :, 0].shape)

    # save back nifti of result with same affine as "output_filename"
    #nib.Nifti1Image(Sig_TE, affine).to_filename('S_TE.nii')

    print("--- %s seconds ---" % (time.time() - start_time))
    "---- Header End ----"

