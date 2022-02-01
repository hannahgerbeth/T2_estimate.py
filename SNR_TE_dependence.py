import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import time


def Sig2Noise_TE(Signal_TE, sigmamap):
    SNR_TE = np.zeros(Signal_TE.shape)

    for i in range(Signal_TE.shape[3]):
        SNR_TE[:, :, :, i] = Signal_TE[:, :, :, i] / sigmamap
    return SNR_TE


"""------------------------------TEST-------------------------------------"""

if __name__ == '__main__':
    start_time = time.time()

    # load noisemap nifti "mask_filename"
    sigmamap_img = nib.load('noise_sigmas.nii')
    temp_sigma_map = sigmamap_img.get_fdata()
    sigma_map = np.transpose(temp_sigma_map, (2, 0, 1))
    affine = sigmamap_img.affine


    # load S(TE) nifti "mask_filename"
    SigTE_img = nib.load('S_TE.nii')
    S_TE = SigTE_img.get_fdata()
    # affine = S_TE.affine

    # load mask nifti "mask_filename"
    mask_img = nib.load('mask.nii')
    mask_temp = mask_img.get_fdata().astype(np.bool)  # change type to boolean
    mask = np.transpose(mask_temp, (2, 0, 1))

    print('sigmamap', sigma_map.shape)
    print('S_TE', S_TE.shape)
    print('mask', mask.shape)

    snr_TE = Sig2Noise_TE(S_TE, sigma_map)

    # save back nifti of result with same affine as "output_filename"
    #nib.Nifti1Image(snr_TE, affine).to_filename('snr_TE.nii')


    plt.plot(snr_TE[60, 40, 25, :])
    plt.show()


    print("--- %s seconds ---" % (time.time() - start_time))
    "---- Header End ----"







