'''
Created on 25Mar.,2017

@author: cac009
'''

import getopt
import sys
from .query_datacube import query_datacube_and_serialize_tiles
from .query_datacube import load_query, query_datacube, datetostring
from yaml import load, dump
import pickle
import os
import datacube
import pandas as pd
import yaml

import logging

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def write_job_script(strrefl, script, job_params, outf, strmask=None,
                     script_options=None):
    """
    Writes a text, job script file to disk.  Has the following format:

    <job params>
    <script> -I <strrefl> -M <strmask> <script options>

    :param strrefl: name of reflectance fille
    :type strrefl: string
    :param script: name of script
    :type script: string
    :param job_params: list of job params
    :type job_params: list of string
    :param outf: name of job file
    :type outf: string
    :param strmask: name of mask file
    :type strmask: string
    :param script_options: script options
    :type script_options: string
    """

    logging.debug(script)
    logging.debug(job_params)
    logging.debug(outf)
    logging.debug(script_options)
    logging.debug(strrefl)
    logging.debug(strmask)

    if (script_options is None):
        script_options = ''

    cmdline = script + ' ' + '-I ' + strrefl

    if (strmask is not None):
        cmdline = cmdline + ' -M ' + strmask

    # write out pbs file
    cmdline = cmdline + ' ' + script_options
    job_params1 = job_params[:]
    job_params1.append('')
    job_params1.append(cmdline)

    with open(outf+'_SCRIPT.sh', 'w') as fid:
        fid.writelines(job_params1)

    return


def pbs_job_setup(query, script, job_params, odir=None,
                  outf_prefix=None, script_options=None,
                  dcconf=None, single=False):
    """
    Performs query on Datacube and serializes (pickles) tiles and writes a "job"
    file.  Each tile has a job script file. The job file (text file) will have
    the following format:

    <job params>
    <script> -I <tile> -M <pq> <script options>

    and is intended to be used for creating job files suitable for submission
    to a batch system of a HPC system.  A job script file is generated for each
    tile serialized.  The query utilizes the Gridworkflow.list_tiles() function

    :param query: spatial and temporal query to be used for searching the
                  Datacube
    :type query: dict
    :param script: name of script to be called from job script
    :type script: string
    :param job_params: params to appear at beginning of job script
    :type job_params: list of string
    :param odir: output directory to which tile will be written
    :type odir: string
    :param outf_prefix: string, with prefix to attach to output files
    :type outf_prefix: string
    :param script_options: options to be passed to script
    :type script_options: string
    :param dcconf:
    :type dcconf:
    :param single:
    :type single: bool
    """

    strrefl_list, strmask_list, tile_info = \
        query_datacube_and_serialize_tiles(query, odir=odir,
                                           outf_prefix=outf_prefix,
                                           single=single)

    if (single is False):

        # multiple files
        for ix in range(len(strrefl_list)-1):
            # setup output name prefix_sensor_date.pkl

            strdate = datetostring(tile_info[ix][-1])
            outf = outf_prefix + '_' + strdate

            if (query['pq'] != None):
                mask = strmask_list[ix]
            else:
                mask = None

            write_job_script(strrefl_list[ix], script, job_params, outf,
                             strmask=mask, script_options=script_options)

    else:
        # single file
            outf = outf_prefix + '_' \
                                + datetostring(tile_info[0][-1]) \
                                + '_' \
                                + datetostring(tile_info[-1][-1])

            if (query['pq'] != None):
                mask = strmask_list
            else:
                mask = None

            write_job_script(strrefl_list, script, job_params, outf,
                             strmask=mask,
                             script_options=script_options)

    return


def pbs_job_setup_main(argv):
    """
    Performs query on Datacube and serializes (pickles) tiles and writes a "job"
    file.  Each tile has a job script file.  The job file (text file) will have
    the following format:

    <job params>
    <script> -I <tile> -M <pq> <script options>

    and is intended to be used for creating job files suitable for submission
    to a batch system of a HPC system.  A job script file is generated for each
    tile serialized.  The query utilizes the Gridworkflow.list_tiles() function

    Usage:

    pbs_job_setup.py -q <query> -s <script> -j <job params>,
                     -o <output dir*> -f <filename output prefix*>,
                     -S <script options*> -z <single tile*>

    *indicate optional

    :param argv: list of command line arguments as detailed below
    :type argv: string

    -q <query> - yaml file containing the query to be passed to GW.list_tiles()
    -s <script> - string with the name of the script to called from with the
                  job file
    -j <job params> - text file containing the job params to be copied into the
                  job file.
    -o <ouput dir> - string specifying output directory for the tile data.
    -f <filename prefix> - string, with prefix to attach to output files
    -S <script options> - text file containing script options
    -z - if present indicates that all tile data are to be written to a single
         file.  Default is to write each tile to its own file

    """

    '''Command line options.'''

    um = ['pbs_job_setup.py -q <query> -s <script> -j <job params>\n',
          '                 -o <output dir*> -f <filename output prefix*>\n',
          '                 -S <script options*> -z *\n',
          '  Note options with * are optional']

    usage_message = ''.join(um)
    odir = None
    outf_prefix = None
    dcconf = None
    single = False

    try:
        opts, args = getopt.getopt(argv, 'hq:s:j:o:f:S:d:z',
                                   ['query', 'script', 'job', 'odir', 'prefix',
                                    'opt', 'single'])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)

    bMandatory = [False] * 3
    for opt, arg in opts:
        if (opt == '-h'):
            print(usage_message)
            sys.exit(2)
        elif opt in ('-q', '--query'):
            # query
            query = load_query(arg)
            bMandatory[0] = True
        elif opt in ('-s', '--script'):
            # script to execute e.g.  'python sambuca_spatial_raijin_dc'
            script = arg
            bMandatory[1] = True
        elif opt in ('-j', '--job'):
            # job paramater e.g. PBS directives...module load...etc
            # this is a file...plain text...read in here
            if (os.path.isfile(arg) == False):
                print('Job parameter file does not exist')
                sys.exit(2)
            with open(arg, 'r') as fid:
                job_params = fid.readlines()
            bMandatory[2] = True
        elif opt in ('-o', '--odir'):
            # directory to write tiles and job scripts
            odir = arg
        elif opt in ('-f', '--prefix'):
            # filename prefix for job scripts and tiles
            outf_prefix = arg
        elif opt in ('-S', '--opt'):
            # script options....this is a plain text file..this option is a
            # file
            # TODO make another option that is just string?
            with open(arg, 'r') as fid:
                script_options = fid.readlines()
            script_options = ''.join(script_options)
        elif opt in ('-d', '--dcconf'):
            # datacube connection settings
            dcconf = arg
        elif opt in ('-z', '--single'):
            # Single file with containing multiple dates
            single = True
        else:
            print('Invalid switch ' + opt)
            sys.exit(2)

    if (all(bMandatory) == False):
        print(bMandatory)
        print('Error missing command line argument ')
        print(usage_message)
        sys.exit(2)

    print('Processing Commenced')

    logging.debug(query)
    logging.debug(script)
    logging.debug(job_params)
    logging.debug(odir)
    logging.debug(outf_prefix)
    logging.debug(script_options)

    flag = pbs_job_setup(query, script, job_params,
                         odir=odir, outf_prefix=outf_prefix,
                         script_options=script_options,
                         dcconf=dcconf, single=single)

    print('Processing complete')

    return


def main():

    pbs_job_setup_main(sys.argv[1:])

    return


if __name__ == '__main__':
    pbs_job_setup_main(sys.argv[1:])
