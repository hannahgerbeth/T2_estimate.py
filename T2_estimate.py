import numpy as np
import nibabel as nib
import time

' T2-map calculation for a given data-set + mask '

def T2_map_calc(mask, data, TE_time, range=(0, 200)):
    # input arrays: data and mask
    # mask has given shape [x, y, z], in this case [120, 80, 50]
    # data has shape (mask.shape[:3] + (K,)) with "K" values in the 4th dimension for our "K" measurements
    # in this case data.shape = [120, 80, 50, 5]
    # 'range' optional argument returns the estimated T2-values only if its between 0 ms and 200 ms, else it is set to 0
    # to avoid extremely high or low (negative) values
    # if range=None all T2 values are returned, no matter what value

    if range:
        T2_fixed_range = np.zeros(data.shape[:3])
        S0_fit = np.zeros(data.shape[:3])
        for xyz in np.ndindex(data.shape[:3]):  # loop in N-dimension, xyz is a tuple (x,y,z)
            if mask[xyz]:
                a, b = np.polyfit(TE_time, np.log(data[xyz]), 1)
                temp = - 1. / a
                S0_fit[xyz] = np.exp(b)
                if temp < range[0] or temp > range[1]:
                    T2_fixed_range[xyz] = 0
                else:
                    T2_fixed_range[xyz] = temp
        return T2_fixed_range, S0_fit

    else:
        T2_map = np.zeros(data.shape[:3])
        S0_fit = np.zeros(data.shape[:3])
        for xyz in np.ndindex(data.shape[:3]):  # loop in N-dimension, xyz is a tuple (x,y,z)
            if mask[xyz]:
                a, b = np.polyfit(TE_time, np.log(data[xyz]), 1)
                T2_map[xyz] = - 1. / a
                S0_fit[xyz] = np.exp(b)
        return T2_map, S0_fit


"""------------------------------TEST-------------------------------------"""

if __name__ == '__main__':
    start_time = time.time()

    """ Get Data from nifit (nii)-Files """
    # bring everything to shape [read, phase, slice] = [120, 80, 50] and make mask align with data

    # load mask nifti "mask_filename"
    mask_img = nib.load('mask.nii')
    temp_mask = mask_img.get_fdata().astype(np.bool)  # change type to boolean
    #print('mask shape', temp_mask.shape)
    mask = np.transpose(temp_mask, (2, 0, 1))
    #print('mask reshape', mask.shape)

    # load data nifti "data_filename" with nibabel
    data_img_89 = nib.load('ACQ_USER_PVMmcw_DWEpiWavev7X89P1.nii')
    data_89 = data_img_89.get_fdata()
    affine = data_img_89.affine
    #print('data shape', data_89.shape)

    # transpose data to make it align with mask
    data_89_TE_40 = np.flip(np.transpose(data_89, (1, 0, 2)), axis=(2, 0))
    #print('data reshape', data_89_TE_40.shape)

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
    print(data_93_TE_100.shape)

    """ T2 map estimation """

    # echo times in ms
    TE_time = np.array([40, 50, 60, 70, 100])
    # data_array arranged in shape (80, 50, 120, 5)
    data_decay = np.transpose(np.array([data_89_TE_40, data_90_TE_50, data_91_TE_60, data_92_TE_70, data_93_TE_100]),
                              (1, 2, 3, 0))

    print('data decay', data_decay.shape)

    #print('full data', data_decay.shape)
    # plt.imshow(data_decay[40, :, :, 4], cmap='gray')
    # plt.show()
    # plt.imshow(mask[40, :, :], cmap='gray')
    # plt.show()

    ' single value test run '

    """
    #coef = np.polyfit(TE_time, np.log(data_decay[40, 25, 60, : ]/data_89_TE_40[40, 25, 60]),1)
    #poly1d_fn = np.poly1d(coef) # poly1d_fn is now a function which takes in x and returns an estimate for y

    # y = a + bx
    # ln(I) = ln(I_0) + (-1/T2) t
    # a = - 1/T2 -> T2 = -1/a
    # b = ln(I_0) -> I_0 = exp(b)
    a, b = np.polyfit(TE_time, np.log(data_decay[40, 25, 60, : ]), 1)
    print('a', a, 'b', b)
    print('T2', - 1/a, 'ms')
    print('I_0', np.exp(b))

    #plt.plot(TE_time, np.log(data_decay[40, 25, 60, : ]/data_89_TE_40[40, 25, 60]), 'yo', TE_time, poly1d_fn(TE_time), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
    #plt.show()
    """

    ' T2-map calculation for a given data-set + mask '

    T2_map, S0_fit = T2_map_calc(mask, data_decay, TE_time, range=None)
    T2_map_fixed_range = T2_map_calc(mask, data_decay, TE_time, range=(0, 250))[0]

    # save back nifti of result with same affine as "output_filename"
    #nib.Nifti1Image(T2_map, affine).to_filename('T2_map.nii')
    #nib.Nifti1Image(T2_map_fixed_range, affine).to_filename('T2_map_fixed_range_from_0_to_250ms.nii')
    #nib.Nifti1Image(S0_fit, affine).to_filename('S0_fromT2fit.nii')

    print(T2_map.shape, 'T2 in Voxel [60, 40, 25]', T2_map[60, 40, 25])
    print(S0_fit.shape, 'S0 in Voxel [60, 40, 25]', S0_fit[60, 40, 25])
    print(T2_map_fixed_range.shape, 'Voxel [60, 40, 25]', T2_map_fixed_range[60, 40, 25])

    print("--- %s seconds ---" % (time.time() - start_time))
    "---- Header End ----"


