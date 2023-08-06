'''
Created on 29Apr.,2017

@author: cac009
'''
from datacube.storage import masking


def default_refl_mask(ref_data):
    """
    Example of masking using the reflectance.

    :param ref_data: reflectance dataset from which to derive mask
    :type ref_data: xarray
    :rtype 2D numpy array (BOOL)
    """
    #print('blue')
    #print(ref_data.blue)
    blue = ref_data.blue.where(ref_data.blue != ref_data.blue.attrs['nodata'])
    nir = ref_data.nir.where(ref_data.nir != ref_data.nir.attrs['nodata'])

    # blue and red are xarray data array's
    ratio = ((blue - nir) / (nir + blue))
    mask = ratio > 0.0

    # returns numpy array   shape (y,x)
    mask = mask.values.squeeze()

    return mask


def default_pqa_mask(pqa_data):
    """
    Example of masking using datacube masking function and default Landsat PQA
    layer..assumption the dataset only has one time slice

    :param pqa_data:
    :type xarray:
    :rtype 2D numpy array (bool)
    """
    # contiguous = masking.make_mask(pq_data, contiguous=1).pixelquality

    mask = masking.make_mask(pqa_data.pixelquality,
                             cloud_acca='no_cloud',
                             cloud_shadow_acca='no_cloud_shadow',
                             cloud_fmask='no_cloud',
                             cloud_shadow_fmask='no_cloud_shadow',
                             contiguous=True,
                             blue_saturated=False,
                             green_saturated=False,
                             red_saturated=False)

    # returns numpy array   shape (y,x)
    mask = mask.values.squeeze()

    return mask
