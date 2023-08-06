'''
Created on 11Apr.,2017

@author: cac009
'''
import getopt
import os
import pickle
import sys
import yaml
import pandas as pd
import datacube
from .load_config_file import load_config_file, check_for_keys
import sambuca_core as sbc
from datacube.api import GridWorkflow
import rasterio
import multiprocessing as mp
import numpy.ma as ma
import imp

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

import xarray as xr

from swampy.sen2coral import sambuca_input_rrs
from swampy.sen2coral import sambuca_input_parameters
from swampy.sen2coral import sambuca_preparation
from swampy.sen2coral import sambuca_calculations
from swampy.sen2coral import sambuca_outputs
from swampy.sen2coral import define_outputs
import time

from .sam_com_multi_process import sam_com_mp

import sambuca_core as sbc
from collections import defaultdict

from datacube.utils.geometry import CRS

import logging

DEBUG = False

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_model_params_config_file(arg):
    """
    Loads SWAMpy model parameters from yaml file.  Check for errors (missing
    keys)

    :param arg: name of yaml file containing model parameters
    :type arg: string
    :return SWAMpy model parameters read from file
    :rtype dict
    :raises ValueError raised if all parameters are not present
    """

    if (os.path.isfile(arg) == False):
        raise IOError("specified file %s does not exist" % arg)

    with open(arg,  'r') as fid:
        dict_config = yaml.safe_load(fid)

    try:
        key_check_list = ['free_params', 'fixed_params', 'envmeta', 'shallow']
        check_for_keys(dict_config, key_check_list)

        key_check_list = ['p_min', 'p_max']
        check_for_keys(dict_config['free_params'], key_check_list)

        key_check_list = ['cdom', 'chl', 'depth', 'nap', 'sub1_frac',
                          'sub2_frac', 'sub3_frac']
        check_for_keys(dict_config['free_params']['p_min'], key_check_list)
        check_for_keys(dict_config['free_params']['p_max'], key_check_list)

        key_check_list = ['sub1_frac', 'sub2_frac', 'sub3_frac',
                          'chl', 'cdom', 'nap', 'depth',
                          'a_cdom_slope', 'a_nap_slope', 'bb_ph_slope',
                          'bb_nap_slope', 'lambda0cdom', 'lambda0nap',
                          'lambda0x', 'x_ph_lambda0x', 'x_nap_lambda0x',
                          'a_cdom_lambda0cdom', 'a_nap_lambda0nap',
                          'bb_lambda_ref', 'water_refractive_index']
        check_for_keys(dict_config['fixed_params'], key_check_list)

        key_check_list = ['off_nadir', 'q_factor', 'theta_air']
        check_for_keys(dict_config['envmeta'], key_check_list)
    except ValueError as e:
        raise ValueError('specified file %s has an error %s' % (arg, str(e)))

    return dict_config


def load_swampy_config_files(input_options=None, output_options=None,
                             siops_datasets=None, sensor_data=None,
                             model_params=None, optz_params=None):
    """
    Loads yaml configuration files used in the SWAMpy calculation.

    :param input_options: name of input options file
    :type input_options: string
    :param output_options: name of output options file
    :type output_options: string
    :param siops_datasets: name of siops file
    :type siops_datasets: string
    :param sensor_data: name of sensor file
    :type sensor_data: string
    :param model_params: name of model params file
    :type model_params: string
    :param optz_params: name of optimization file
    :type optz_params: string
    :return returns dictionary of processing options
    :rtype dict
    """

    INPUT_DF_KEYS = ['measurements', 'mask_module_file', 'mask_pq_func',
                     'mask_refl_func', 'rrs']
    OUTPUT_DF_KEYS = ['odir', 'prefix', 'suffix', 'format', 'options']
    SIOP_DF_KEYS = ['substrate_db', 'substrate_names', 'aphy_star_db',
                    'aphy_star_name', 'awater_db', 'awater_name']
    SENSOR_DF_KEYS = ['sensor_filter_db', 'sensor_filter_name', 'nedr_db',
                      'nedr_name']
    MODEL_DF_KEYS = ['free_params', 'p_min', 'p_max', 'cdom', 'chl', 'depth',
                     'nap', 'sub1_frac', 'sub2_frac', 'sub3_frac',
                     'fixed_params', 'sub1_frac', 'sub2_frac', 'sub3_frac',
                     'chl', 'cdom', 'nap', 'depth', 'a_cdom_slope',
                     'a_nap_slope', 'bb_ph_slope', 'bb_nap_slope',
                     'lambda0cdom', 'lambda0nap', 'lambda0x', 'x_ph_lambda0x',
                     'x_nap_lambda0x', 'a_cdom_lambda0cdom',
                     'a_nap_lambda0nap',
                     'bb_lambda_ref', 'water_refractive_index',
                     'envmeta', 'off_nadir', 'q_factor', 'theta_air',
                     'shallow']
    OPTZ_DF_KEYS = ['method', 'maxiter', 'disp', 'pool']

    rdict = {'input_options': None, 'output_options': None,
             'siops_datasets': None, 'sensor_data': None,
             'model_params': None, 'optz_params': None}

    if (input_options is not None):
        rdict['input_options'] = load_config_file(input_options, INPUT_DF_KEYS)

    if (output_options is not None):
        rdict['output_options'] = load_config_file(output_options,
                                                   OUTPUT_DF_KEYS)

    if (siops_datasets is not None):
        rdict['siops_datasets'] = load_config_file(siops_datasets,
                                                   SIOP_DF_KEYS)
        # need to do this as load_spectral_library returns names in lower case
        '''
        rdict['siops_datasets']['aphy_star_name'] = \
            rdict['siops_datasets']['aphy_star_name'].lower()

        rdict['siops_datasets']['awater_name'] = \
            rdict['siops_datasets']['awater_name'].lower()
        rdict['siops_datasets']['substrate_names'] = \
             [x.lower() for x in rdict['siops_datasets']['substrate_names']]
        '''

    if (sensor_data is not None):
        rdict['sensor_data'] = load_config_file(sensor_data, SENSOR_DF_KEYS)
        # need to do this as load_spectral_library returns names in lower case
        rdict['sensor_data']['nedr_name'] = \
            rdict['sensor_data']['nedr_name'].lower()

    if (model_params is not None):
        rdict['model_params'] = load_model_params_config_file(model_params)

    if (optz_params is not None):
        rdict['optz_params'] = load_config_file(optz_params, OPTZ_DF_KEYS)

    return rdict


def sam_obs(base_path, Rrs=False, param_dict=None):
    """
    Loads the reflectance file and sets up the image info data structures.
    Loads the sensor data. Modified version of sam_obs found in sen2coral.
    Uses Datacube API function Gridworkflow.load() to load reflectance data

    :param base_path:
    :type base_path:
    :param Rrs: -
    :type Rrs:
    :param param_dict: contains
    :type param_dict: dict
    :return observed_rrs: reflectance data
    :rtype observed_rrs: xarray dataset
    """

    # TODO: would make sense to merge this with the sen2coral version
    observed_rrs_filename = ''

    sensor = param_dict['sensor']
    logging.debug(sensor)

    measurements = param_dict['measurements']
    refl_tile_id = param_dict['refl_tile_id']
    sensor_filters = sbc.load_sensor_filters(sensor['sensor_filter_db'])
    # retrieve the specified filter
    sensor_filter = sensor_filters[sensor['sensor_filter_name']]
    # SPECIFY NEDR values e.g lib:bandname or for csv file:columheader
    nedr = sbc.load_spectral_library(sensor['nedr_db'], validate=False)
    logging.debug(nedr)
    nedr = nedr[sensor['nedr_name']]

    # returns an xarray dataset ...xarray datasets contain xarray DataArrays
    # DataArrays can be cast to numpy arrays
    observed_rrs = GridWorkflow.load(refl_tile_id, measurements=measurements)
    # print(observed_rrs.blue)

    observed_rrs_width = refl_tile_id.geobox.width
    observed_rrs_height = refl_tile_id.geobox.height
    # number of bands
    count = len(measurements)
    # list of integer band identifers
    indexes = tuple(range(1, count+1))

    # datacube.model.CRS, rasterio returns -> rasterio.crs.CRS
    code = int(refl_tile_id.geobox.crs.crs_str[-4:])
    crs = rasterio.crs.CRS.from_epsg(code)
    # crs = refl_tile_id.geobox.crs
    # affine.Affine, same as what rasterio src.affine returns
    affine = refl_tile_id.geobox.affine

    # If Above surface remote sensing reflectance (Rrs) tag is true, convert to
    # below surface (rrs) after Lee et al. (1999)
    '''
    if Rrs is True:
        # xarray dataset handles this it broadcasts across attributes
        observed_rrs = (2*observed_rrs)/((3*observed_rrs)+1)
    '''

    image_info = {'observed_rrs_width': observed_rrs_width,
                  'observed_rrs_height': observed_rrs_height, 'crs': crs,
                  'affine': affine, 'count': count, 'indexes': indexes,
                  'nedr': nedr, 'sensor_filter': sensor_filter,
                  'base_path': base_path,
                  'observed_rrs_filename': observed_rrs_filename}

    # returns an xarray dataset...observed_rss

    return observed_rrs, image_info


def load_sensor_data(observed_rrs, param_dict=None):
    """
    Loads the sensor data and sets up the image info data structures.

    :param observed_rrs: reflectance dataset to which SWAMpy is to be applied
    :type observed_rrs: xarray dataset as returned by Datacube.load()
    :param param_dict:  holds name of sensor
    :type param_dict: dict
    :return image_info: image info
    :rtype image_info: dict
    """

    # copy of sam_obs but without the load reflectance image
    # TODO: refactor and merge with sam_obs
    observed_rrs_filename = ''

    sensor = param_dict['sensor']
    logging.debug(sensor)

    sensor_filters = sbc.load_sensor_filters(sensor['sensor_filter_db'])
    # retrieve the specified filter
    sensor_filter = sensor_filters[sensor['sensor_filter_name']]
    # SPECIFY NEDR values e.g lib:bandname or for csv file:columheader
    nedr = sbc.load_spectral_library(sensor['nedr_db'], validate=False)
    logging.debug(nedr)
    nedr = nedr[sensor['nedr_name']]

    observed_rrs_width = observed_rrs.geobox.width
    observed_rrs_height = observed_rrs.geobox.height
    # number of bands
    count = len(observed_rrs.data_vars)
    # list of integer band identifers
    indexes = tuple(range(1, count+1))

    # datacube.model.CRS, rasterio returns -> rasterio.crs.CRS
    code = int(observed_rrs.geobox.crs.crs_str[-4:])
    crs = rasterio.crs.CRS.from_epsg(code)
    # crs = refl_tile_id.geobox.crs
    # affine.Affine, same as what rasterio src.affine returns
    affine = observed_rrs.geobox.affine

    image_info = {'observed_rrs_width': observed_rrs_width,
                  'observed_rrs_height': observed_rrs_height, 'crs': crs,
                  'affine': affine, 'count': count, 'indexes': indexes,
                  'nedr': nedr, 'sensor_filter': sensor_filter,
                  'base_path': '',
                  'observed_rrs_filename': observed_rrs_filename}

    # returns an xarray dataset...observed_rss

    return image_info


def load_pq_data(mask_tile_id):
    """
    Loads the dataset, from the Datacube, that is to be used for masking
    purposes

    :param mask_tile_id: tile to be loaded from the Datacube
    :type mask_tile_id: a dict as returned by GridWorkflow.list_tiles
    :return: dataset to be used for masking purposes
    :rtype: xarray dataset
    """

    qa_xarray = None

    # load qa image - load and process
    if (mask_tile_id is not None):
        # assuming mask data is single band
        qa_xarray = GridWorkflow.load(mask_tile_id)

    return qa_xarray


def derive_mask(qa_xarray, rdata_xarray, mask_qa_func, mask_refl_func):
    """
    Given QA or Refl data or both calculate a mask to be used for constraining
    the calculation of SWAMpy to only valid pixels.

    :param qa_xarray: PQ data to be used in calculation of a mask
    :type qa_xarray: xarray dataset
    :param rdata_xarray: Ref data to be used in calculation of a mask
    :type rdata_xarray: xarray dataset
    :param mask_qa_func: Function to use to calculate mask from QA data
    :type mask_qa_func: pointer to function or None
    :param mask_refl_func: Function to use to calculate mask from ref data
    :type mask_refl_func: pointer to function or None
    :return mask to use to constrain calculation.  If pixel==True then process
    :rtype 2D numpy array (BOOL).  Returns None if strmask_qa_func and not
    supplied strmask_refl_func
    """

    mask = None

    if (qa_xarray is not None):
        if (mask_qa_func is not None):
            # return bool numpy array shape (y,x)
            bqa_mask = mask_qa_func(qa_xarray)
            mask = bqa_mask

    # mask image defined on reflectance image
    if (mask_refl_func is not None):
        brefl_mask = mask_refl_func(rdata_xarray)
        if (mask is not None):
            mask = mask * brefl_mask
        else:
            mask = brefl_mask

    return mask


def setup_output_dir(odir, filename, overwrite=False):
    """
    Setup output directory. Check if output file already exists

    :param odir:
    :type odir:
    :param filename:
    :type filename:
    """

    if (os.path.exists(odir) == False):
        # diretory does not exist therefore make path
        os.makedirs(odir)
    else:
        if (os.path.isdir(odir) == False):
            raise IOError("Specified output directory %s is a file" % odir)

    strf = odir+filename
    if (os.path.isfile(strf) == True):
        if (overwrite is False):
            raise IOError("Specified file already exists %s\n" % strf)

    return strf


def write_to_netcdf_results(results_recorder, coords, dims, attrs, odir,
                            filename, overwrite=False):
    """
    Output SWAMpy results to netCDF file.

    :param results_recorder: SWAMpy results for image
    :type results_recorder: class ArrayResultWriter see Sambuca documentation
    :param coords: coords for the netcdf file
    :type coords: dict {'time','y','x'}
    :param dims: dimension labels for netcdf file
    :type dims: tuple (time, y, x)
    :param attrs: attributes
    :type attrs: dict
    :param odir: output directory
    :type odir: string
    :param filename: output filename
    :type filename: string
    :param overwrite: overwrite file if file already exists. True=>overwrite
    :type overwrite: bool
    """
    overwrite = True
    strf = setup_output_dir(odir, filename, overwrite=overwrite)

    rr = results_recorder

    out_da = {}
    nax = np.newaxis

    t_abun = rr.sub1_frac + rr.sub2_frac + rr.sub3_frac
    # print(t_abun.shape)
    out_da['chl'] = xr.DataArray(rr.chl[nax], coords=coords, dims=dims)
    out_da['cdom'] = xr.DataArray(rr.cdom[nax], coords=coords, dims=dims)
    out_da['nap'] = xr.DataArray(rr.nap[nax], coords=coords, dims=dims)
    out_da['depth'] = xr.DataArray(rr.depth[nax], coords=coords, dims=dims)

    out_da['sub1_frac'] = xr.DataArray(rr.sub1_frac[nax], coords=coords,
                                       dims=dims)
    out_da['sub2_frac'] = xr.DataArray(rr.sub2_frac[nax], coords=coords,
                                       dims=dims)
    out_da['sub3_frac'] = xr.DataArray(rr.sub3_frac[nax], coords=coords,
                                       dims=dims)

    out_da['total_abun'] = xr.DataArray(t_abun[nax], coords=coords, dims=dims)

    # print (out_da['total_abun'] )
    # print (out_da['sub1_frac'] )

    out_da['sub1_frac_norm'] = out_da['sub1_frac'] / out_da['total_abun']
    out_da['sub2_frac_norm'] = out_da['sub2_frac'] / out_da['total_abun']
    out_da['sub3_frac_norm'] = out_da['sub3_frac'] / out_da['total_abun']

    out_da['kd'] = xr.DataArray(rr.kd[nax], coords=coords, dims=dims)
    out_da['sdi'] = xr.DataArray(rr.sdi[nax], coords=coords, dims=dims)

    out_da['error_f'] = xr.DataArray(rr.error_f[nax], coords=coords, dims=dims)
    out_da['error_lsq'] = xr.DataArray(rr.error_lsq[nax], coords=coords,
                                       dims=dims)
    out_da['error_alpha'] = xr.DataArray(rr.error_alpha[nax], coords=coords,
                                         dims=dims)
    out_da['error_alpha_f'] = xr.DataArray(rr.error_alpha_f[nax],
                                           coords=coords,
                                           dims=dims)
    out_da['nit'] = xr.DataArray(rr.nit[nax], coords=coords, dims=dims)
    out_da['success'] = xr.DataArray(rr.success[nax] < 1, coords=coords,
                                     dims=dims)

    # Closed_rrs 3D numpy array
    dims3D = ('z',) + dims
    coords['z'] = np.arange(rr.closed_rrs.shape[-1])
    closed_rrs = np.transpose(rr.closed_rrs[nax], (3, 0, 1, 2))
    out_da['closed_rrs'] = xr.DataArray(closed_rrs, coords=coords,
                                        dims=dims3D)

    results = xr.Dataset(out_da, attrs=attrs)
    results.to_netcdf(strf, mode='w', format='NETCDF4')
    results.close()

    return


def write_to_netcdf_inputs(refl,  coords, dims, attrs, odir,
                           filename, overwrite=False, pq=None, mask=None):
    """
    Write input files (refl, pq, mask etc) used in SWAMpy calculation to netCDF
    file.  Single file for all inputs.  Primarily used for debugging purposes

    :param refl: reflectance data used in calculation
    :type refl: numpy 3D array
    :param pq: PQ data used in calculation
    :type pq: numpy 2D array
    :param mask: mask generated from PQ
    :type mask: numpy 2D array
    :param coords: coords for the netcdf file
    :type coords: dict {'time','y','x'}
    :param dims: dimension labels for netcdf file
    :type dims: tuple (time, y, x)
    :param attrs: attributes
    :type attrs: dict
    :param odir: output directory
    :type odir: string
    :param filename: output filename
    :type filename: string
    :param overwrite: overwrite file if file already exists. True=>overwrite
    :type overwrite: bool
    """
    overwrite = True
    strf = setup_output_dir(odir, filename, overwrite=overwrite)

    out_da = {}
    nax = np.newaxis

    if (pq is not None):
        out_da['pq'] = xr.DataArray(pq, coords=coords, dims=dims)
    if (mask is not None):
        out_da['mask'] = xr.DataArray(mask[nax], coords=coords, dims=dims)
    dims3D = ('z',) + dims
    coords['z'] = np.arange(refl.shape[0])

    refl = np.transpose(refl[nax], (1, 0, 2, 3))
    out_da['refl'] = xr.DataArray(refl, coords=coords, dims=dims3D)

    results = xr.Dataset(out_da, attrs=attrs)
    results.to_netcdf(strf, mode='w', format='NETCDF4')
    results.close()

    return


def swampy_spatial_datacube_jpnb(refl_xr, in_opt, out_opt, siops_datasets,
                                 sensor_data, model_params, optz_params,
                                 pq_xr=None):
    """
    Applies SWAMpy to multiple reflectance dataset (xarrays), optionally
    constraining the calculation to pixels specified by a mask. Outputs the
    SWAMpy results to netcdf file (one file per time slice containing all of the
    SWAMpy outputs).  Geared towards use with interactive environments, Juypter
    notebokks etc

    :param refl_xr: reflectance dataset(s) to apply SWAMpy algorithmn
    :type refl_xr: xarray dataset, as returned by Datacube.load() function
    :param in_opt: input processing options- mask function, refl calculation etc
    :type in_opt: dict
    :param out_opt: output processing options- output dir and format
    :type out_opt: dict
    :param siops_datasets: name of siops datasets- substrate etc
    :type siops_datasets: dict
    :param sensor_data: name of sensor datasets- filter function etc
    :type sensor_data: dict
    :param model_params: SWAMpy model parameters
    :type model_params: dict
    :param optz_params: optimization parameters- #iteraions number, #cores
    :type optz_params: dict
    :param pq_xr: dataset(s) used to generate mask from. Typically the PQ
                  product
    :type pq_xr: xarray dataset, as returned by Datacube.load() function
    """

    # TODO: retrieve scale factor from data
    SCALE_FACTOR = 10000.0

    date_list = refl_xr.coords['time'].values
    for idate in date_list:

        observed_rrs = refl_xr.sel(time=idate)
        pq = None
        # check if there is a matching PQ product for this refl dataset
        if (pq_xr is not None):
            try:
                # refl_xr and pq_xr may be different in terms of dates
                pq = pq_xr.sel(time=idate)
            except KeyError as e:
                # if refl_date not in pq_xr just continue on
                pass

        # dimension, .values returns numpy.datetime64,  convert this to string,
        # use panda to get nicely formated string.
        tmp = str(observed_rrs.coords['time'].values)
        date = pd.to_datetime(tmp)
        strdate = date.strftime('%Y-%m-%d')
        out_fname = out_opt['prefix'] + strdate + out_opt['suffix']

        # Load sensor data
        param_dict = {'sensor': sensor_data}
        # TODO: Error checking
        image_info = load_sensor_data(observed_rrs, param_dict=param_dict)

        coords = observed_rrs.coords
        crs_string = observed_rrs.geobox.crs.crs_str

        # Create mask
        # mask returns numpy array...bool
        mask = derive_mask(pq, observed_rrs, in_opt['mask_pq_func'],
                           in_opt['mask_refl_func'])

        # convert xarray dataset to 3D numpy array
        observed_rrs = observed_rrs.to_array(dim='z').values
        # print('Size of image: ')
        # print(observed_rrs.shape)

        # Do the reflectance calculation ---
        #     see swampy calc. ...replicated here as the algorithm
        #     data to below-surface remote sensing reflectance (rrs)
        # TODO: remove hard coded value and replace with value from yaml file
        #in_opt['rrs'] = True
        if (in_opt['rrs'] == True):
            observed_rrs = observed_rrs / SCALE_FACTOR
            q_factor = model_params['envmeta']['q_factor'] # q = 4?
            observed_rrs = (0.54*observed_rrs)/(0.7*q_factor)
            observed_rrs = (2*observed_rrs)/((3*observed_rrs)+1)

        # Load the parameters -
        #                    substrates, aphystar, awater, pmin, pmax, envdata
        # TODO: maybe ...may make sense to put in read of yaml files
        #                     in this module(?)...
        param_dict = {'siop_datasets': siops_datasets,
                      'model_params': model_params}
        [siop, envmeta] = \
            sambuca_input_parameters.sam_par('', param_dict=param_dict)

        # Prepare the data - unchanged
        [wavelengths, siop, image_info, fixed_parameters,
         result_recorder, objective] = \
            sambuca_preparation.sam_prep(siop, envmeta, image_info)

        t0 = time.time()

        # Do SWAMpy calculation, code is parallelized
        [result_recorder, coordinates, num_pixels] = \
                         sam_com_mp(observed_rrs, objective, siop,
                                          result_recorder, image_info,
                                          mask=mask,
                                          shallow=model_params['shallow'],
                                          method=optz_params['method'],
                                          maxit=optz_params['maxiter'],
                                          pool=optz_params['pool'])

        t1 = time.time()
        print("*******Total execution time: {0:.1f} seconds".format(t1-t0))

        # Output the results
        if (out_opt['format'] == 'gtiff'):
            # all product are indvidual files
            define_outputs.output_suite(result_recorder, image_info,
                                        coordinates, path=out_opt['odir'],
                                        filename=out_fname)
        elif (out_opt['format'] == 'netcdf'):
            # Output to netCDF, all SWAMpy outputs, one netCDF for each date
            # coords time may have to be values
            ow = True
            coord1 = {'time': np.array([coords['time'].values],
                                       dtype='datetime64'),
                      'y': coords['y'].drop('time'),
                      'x': coords['x'].drop('time')}

            dims1 = ('time', 'y', 'x')
            ymodel_params = yaml.dump(model_params)
            attrs = {'crs': crs_string, 'model': ymodel_params}
            write_to_netcdf_results(result_recorder, coord1, dims1, attrs,
                            out_opt['odir'], out_fname+'.nc', overwrite=True)
            if (DEBUG):
                # coords time may have to be values
                coord1 = {'time': np.array([coords['time'].values],
                                       dtype='datetime64'),
                      'y': coords['y'].drop('time'),
                      'x': coords['x'].drop('time')}
                # just coords will suffice but dims must be specified as below
                dims1 = ('time', 'y', 'x')
                if (pq is not None):
                    # print(pq)
                    pq = pq.to_array(dim='z').values
                write_to_netcdf_inputs(observed_rrs, coord1,
                                       dims1, attrs, out_opt['odir'],
                                       out_fname+'_inputs.nc',
                                       overwrite=True, pq=pq, mask=mask)

        # Deallocate space used by refl image and mask
        observed_rrs = 0
        mask = 0
        result_recorder = 0

    return


def swampy_spatial_datacube(refl_tile_list, in_opt, out_opt, siops_datasets,
                            sensor_data, model_params, optz_params,
                            mask_tile_list=None):
    """
    Applies SWAMpy to multiple reflectance tiles,  optionally constraining the
    calculation to pixels specified by a mask. Outputs the SWAMpy results to
    netcdf file (one file per time slice containing all of the SWAMpy outputs).
    Geared towards use with NCI Raijin.

    :param refl_tile_list: list of "reflectance" tiles to process
    :type refl_tile_list: list of tiles as returned by GridWorkflow.list_tiles()
    :param in_opt: input processing options- mask function, refl calculation etc
    :type in_opt: dict
    :param out_opt: output processing options- output dir and format
    :type out_opt: dict
    :param siops_datasets: name of siops datasets- substrate etc
    :type siops_datasets: dict
    :param sensor_data: name of sensor datasets- filter function etc
    :type sensor_data: dict
    :param model_params: SWAMpy model parameters
    :type model_params: dict
    :param optz_params: optimization parameters- #iteraions number, #cores
    :type optz_params: dict
    :param mask_tile_list: list of tiles to use for masking process.
                          Typically the PQ product
    :type mask_tile_list: list of tiles as returned by GridWorkflow.list_tiles()
    """

    # TODO: retrieve scale factor from data
    SCALE_FACTOR = 10000.0

    for ix in range(len(refl_tile_list)):

        refl_tile_id = refl_tile_list[ix]
        # assumes there is a one to one matching between refl and mask list
        # missing PQ products handled by the setup code so this should always
        # be the case.  Missing PQ products are set to None
        if (mask_tile_list is not None):
            mask_tile_id = mask_tile_list[ix]
        else:
            mask_tile_id = None

        # refl_tile_id.sources.coords['time'] returns xarray DataArray,
        # only one time slice so remove
        # dimension, .values returns numpy.datetime64,  convert this to string,
        # use panda to get nicely formated string.
        tmp = \
            str(refl_tile_id.sources.coords['time'].squeeze(dim='time').values)
        date = pd.to_datetime(tmp)
        strdate = date.strftime('%Y-%m-%d')
        out_fname = out_opt['prefix'] + strdate + out_opt['suffix']

        # copy into swampy spatial dc...later date may want to be merged into
        # swampy depending on design goals of swampy...
        # replicated in swampy_spatial_dc
        # allow swampy project to be independant of datacube project
        # 'siop_datasets':siops_datasets

        # returns an xarray dataset...xarray datasets contain xarray DataArrays
        # DataArrays can be cast to numpy arrays
        param_dict = {'sensor': sensor_data,
                      'measurements': in_opt['measurements'],
                      'refl_tile_id': refl_tile_id}
        # TODO: Error checking
        # Load the reflectance data
        [observed_rrs, image_info] = sam_obs('', Rrs=False,
                                             param_dict=param_dict)

        coords = observed_rrs.coords
        crs_string = observed_rrs.crs.crs_str

        # load pq data used for masking
        pq = load_pq_data(mask_tile_id)
        # mask returns numpy array...bool
        mask = derive_mask(pq, observed_rrs,
                           in_opt['mask_pq_func'], in_opt['mask_refl_func'])

        # convert xarray dataset to numpy array
        observed_rrs = \
            observed_rrs.to_array(dim='z').squeeze(dim='time').values
        # Do the reflectance calculation ---
        #   see swampy calc. ...replicated here as the algorithm
        #   supplied for deriving mask more likely expecting vanilla reflectance
        #   data as opposed to below-surface remote sensing reflectance (rrs)
        # TODO: remove hard coded value and replace with value from yaml file
        #in_opt['rrs'] = True
        if (in_opt['rrs'] == True):
            observed_rrs = observed_rrs / SCALE_FACTOR
            q_factor = model_params['envmeta']['q_factor'] # q = 4?
            observed_rrs = (0.54*observed_rrs)/(0.7*q_factor)
            observed_rrs = (2*observed_rrs)/((3*observed_rrs)+1)

        # Load the parameters -
        #                    substrates, aphystar, awater, pmin, pmax, envdata
        # TODO: maybe ...may make sense to put in read of yaml files
        #                     in this module(?)...
        param_dict = {'siop_datasets': siops_datasets,
                      'model_params': model_params}
        [siop, envmeta] = \
            sambuca_input_parameters.sam_par('', param_dict=param_dict)

        # Prepare the data - unchanged
        [wavelengths, siop, image_info, fixed_parameters,
         result_recorder, objective] = \
            sambuca_preparation.sam_prep(siop, envmeta, image_info)

        t0 = time.time()

        # Do SWAMpy calculation, code is parallelized
        [result_recorder, coordinates, num_pixels] = \
                         sam_com_mp(observed_rrs, objective, siop,
                                          result_recorder, image_info,
                                          mask=mask, shallow=model_params['shallow'],
                                          method=optz_params['method'],
                                          maxit=optz_params['maxiter'],
                                          pool=optz_params['pool'])

        t1 = time.time()
        print("*******Total execution time: {0:.1f} seconds".format(t1-t0))

        # Output the results
        if (out_opt['format'] == 'gtiff'):
            # all product are indvidual files
            define_outputs.output_suite(result_recorder, image_info,
                                        coordinates, path=out_opt['odir'],
                                        filename=out_fname)
        elif (out_opt['format'] == 'netcdf'):
            # Write to netcdf
            # coords time may have to be values
            coord1 = {'time': coords['time'].values, 'y': coords['y'],
                      'x': coords['x']}
            # just coords will suffice but dims must be specified as below
            dims1 = ('time', 'y', 'x')

            ymodel_params = yaml.dump(model_params)
            attrs = {'crs': crs_string, 'model': ymodel_params}
            write_to_netcdf_results(result_recorder, coord1, dims1, attrs,
                            out_opt['odir'], out_fname+'.nc', overwrite=False)
            if (DEBUG):
                # coords time may have to be values
                coord1 = {'time': coords['time'].values, 'y': coords['y'],
                          'x': coords['x']}
                # just coords will suffice but dims must be specified as below
                dims1 = ('time', 'y', 'x')
                if (pq is not None):
                    pq = pq.to_array(dim='z').squeeze(dim='time').values
                write_to_netcdf_inputs(observed_rrs, coord1,
                                       dims1, attrs, out_opt['odir'],
                                       out_fname+'_inputs.nc',
                                       overwrite=False, pq=pq, mask=mask)

        # Deallocate space used by refl image and mask
        observed_rrs = 0
        mask = 0


    return


def return_pointer_to_func(module_filename, func_name1, func_name2):
    """
    Loads a module and returns a pointer to a function

    :param module_filename: name of module to load
    :type module_filename: string
    :param func_name1: name of function in module to return
    :type func_name1: string or None
    :param func_name2: name of function in module to return
    :type func_name2: string or None
    :rtype <func> or None, <func> or None
    :raises ImportError raised if problems loading module
    """

    func1 = None
    func2 = None

    # separate out name and path and remove .py if present
    base = os.path.basename(module_filename)
    base = os.path.splitext(base)[0]
    path = os.path.dirname(module_filename)

    # will throw ImportError if problem loading module
    f, filename, description = imp.find_module(base, [path])
    mod = imp.load_module(base, f, filename, description)
    if (func_name1 is not None):
        func1 = getattr(mod, func_name1)
    if (func_name2 is not None):
        func2 = getattr(mod, func_name2)
    f.close()

    return func1, func2


def swampy_spatial_main_datacube(argv):
    """
    Applies SWAMpy to multiple tiles.  Typically used when running on
    NCI HPC system Raijin.

    Usage:
        swampy_spatial_datacube.py -I <refl tile list> -M <mask tile list*>
                                    -i <input_options> -o <output_options>
                                   -s <siops_datasets> -r <sensor_datasets>
                                   -m <model_params> -z <optimization_params>

    :param argv: command line arguments.  argv contains the flags as listed
                 below
    :type argv: string

    -I <refl tile list> - name of file containing reflectance dataset(s) to
                          process.  These input tiles are generated by calling
                          calling pbs_job_setup.py (if running on HPC NCI
                          Raijin infrastruture) or query_datacube.py.  Both
                          generate a serialized (pickled) list of reflectance
                          tiles and rely on the Datacube API function
                          GridWorkflow.list_tiles()
    -M <mask tile list> - name of file containing the dataset(s) to be used as
                          mask, typically the Pixel Quality/cloud mask product.
                          Format of the mask file is as above
                          B: -M is optional, not there implies mask list = 0                    .
    -i <input options>  - yaml file containing input options
                         (mask functions, measurements etc)
    -o <output options> - yaml file containing output options
                          (output dir and file format etc)
    -s <siops dataset> -  yaml file containing the name of siops datasets
                          (substrates etc) to use in calculation
    -r <sensor_dataset> - yaml file containing name of sensor dataset
                          (spectral filter function etc) to use in calculation
    -m <model_params>   - yaml file containing SWAMpy model run parameters
    -z <optimization>   - yaml file containing optimization parameters
                          (max number of optimization iterations and number of
                          parallel tasks)

    """

    '''Command line options.'''
    um = ['swampy_spatial_datacube.py ',
          '-I <refl tile list> -M <mask tile list>\n',
          '                 -i <input_options> -o <output_options>\n',
          '                  -s <siops_datasets> -r <sensor_datasets>\n',
          '                 -m <model_params> -z <optimization_params>\n']

    usage_message = ''.join(um)
    mask_tile = None

    try:
        opts, args = getopt.getopt(argv, 'hI:M:i:o:s:r:m:z:',
                                   ['input', 'mask', 'in_opt', 'out_opt',
                                    'siops', 'sensor', 'model', 'optz'])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)

    bMandatory = [False] * 7
    for opt, arg in opts:
        if (opt == '-h'):
            print(usage_message)
            sys.exit(2)
        elif opt in ('-I', '--input'):
            # name of input "reflectance files"
            if (os.path.isfile(arg) == False):
                print('Input reflectance file does not exist %s' % arg)
                sys.exit(2)
            with open(arg, 'rb') as fid:
                refl_tile = pickle.load(fid)
            if (type(refl_tile) is not list):
                refl_tile = [refl_tile]
            bMandatory[0] = True
        elif opt in ('-i', '--in_opt'):
            # Input options
            try:
                in_opt = load_swampy_config_files(input_options=arg)
                in_opt = in_opt['input_options']

                mask_module = in_opt['mask_module_file']
                func_name1 = in_opt['mask_pq_func']
                func_name2 = in_opt['mask_refl_func']
                if (mask_module is not None):
                    func1, func2 = return_pointer_to_func(mask_module,
                                                          func_name1,
                                                          func_name2)
                    in_opt['mask_pq_func'] = func1
                    in_opt['mask_refl_func'] = func2
            # ImportError,
            except Exception as e:
                print(e)
                sys.exit(2)
            bMandatory[1] = True
        elif opt in ('-o', '--out_opt'):
            # Output options
            try:
                out_opt = load_swampy_config_files(output_options=arg)
                out_opt = out_opt['output_options']
            except Exception as e:
                print(e)
                sys.exit(2)
            bMandatory[2] = True
        elif opt in ('-s', '--siops'):
            # siops datasets/databases
            try:
                siops_datasets = load_swampy_config_files(siops_datasets=arg)
                siops_datasets = siops_datasets['siops_datasets']
            except Exception as e:
                print(e)
                sys.exit(2)
            bMandatory[3] = True
        elif opt in ('-m', '--model'):
            # model parameters
            try:
                model_params = load_swampy_config_files(model_params=arg)
                model_params = model_params['model_params']
            except Exception as e:
                print(e)
                sys.exit(2)
            bMandatory[4] = True
        elif opt in ('-z', '--optz'):
            # optimization parameters
            try:
                optz_params = load_swampy_config_files(optz_params=arg)
                optz_params = optz_params['optz_params']
            except Exception as e:
                print(e)
                sys.exit(2)
            bMandatory[5] = True
        elif opt in ('-M', '--mask'):
            # name of input "maks files"
            if (os.path.isfile(arg) == False):
                print('Input pq file does not exist %s' % arg)
                sys.exit(2)
            with open(arg, 'rb') as fid:
                mask_tile = pickle.load(fid)
            if (type(mask_tile) is not list):
                mask_tile = [mask_tile]
        elif opt in ('-r', '--sensor'):
            # sensor nedr datasets/databases
            try:
                sensor_data = load_swampy_config_files(sensor_data=arg)
                sensor_data = sensor_data['sensor_data']
            except Exception as e:
                print(e)
                sys.exit(1)
            bMandatory[6] = True
        else:
            print('Invalid switch ' + opt)
            sys.exit(2)

    if (all(bMandatory) == False):
        print('Error missing command line argument ')
        print(usage_message)
        sys.exit(2)

    print('Processing Commenced')

    # logging.debug(query)

    flag = swampy_spatial_datacube(refl_tile, in_opt, out_opt, siops_datasets,
                                   sensor_data, model_params, optz_params,
                                   mask_tile_list=mask_tile)

    print('Processing complete')

    return


def main():

    swampy_spatial_main_datacube(sys.argv[1:])

    return


if __name__ == '__main__':
    swampy_spatial_main_datacube(sys.argv[1:])
