'''
Created on 15Mar.,2017

@author: cac009
'''
# from docutils.io import InputError

import getopt
import datacube
from .load_config_file import load_config_file
from datacube.api.core import get_bounds
from datacube.model import GeoBox, GeoPolygon, _polygon_from_boundingbox # CRS
from datacube.utils.geometry import CRS

from datacube.model import GridSpec
from rasterio.coords import BoundingBox
from datacube.api import GridWorkflow

from yaml import load, dump
import yaml
import os
import sys
import pprint
import pickle
import pandas as pd

import logging

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def helper_func(boundingbox):
    """
    """

    # version change in API
    # oogeopoly =
    #        GeoPolygon.from_boundingbox(boundingbox, crs=CRS('EPSG:3577'))
    oogeopoly = _polygon_from_boundingbox(boundingbox, crs=CRS('EPSG:3577'))
    o2 = oogeopoly.to_crs(CRS('EPSG:4326'))

    return o2.boundingbox


def datetostring(date):
    """
    Date to string conversion

    :param date: date
    :type date: numpy.datetime64
    :return date formated YY_MM_DD
    :rtype string
    """

    tmp = pd.to_datetime(date)
    return tmp.strftime('%Y_%m_%d')


def load_query(query_file):
    """
    Loads yaml file containing query.

    :param query_file: name of yaml file containing query
    :type query_file: string
    :return query parameters
    :rtype dict
    """

    QUERY_DF_KEYS = ['ul_latlon', 'lr_latlon', 'start_date',
                     'end_date', 'refl', 'pq', 'dcconf']

    query = load_config_file(query_file, QUERY_DF_KEYS)

    query['ul_latlon'] = tuple(query['ul_latlon'])
    query['lr_latlon'] = tuple(query['lr_latlon'])

    return (query)


def create_dir(odir):
    """
    Create output directory
    """

    # make output dir
    old_dir = os.getcwd()
    if (odir is not None):
        if (os.path.exists(odir) == False):
            # diretory does not exist therefore make path
            os.makedirs(odir)
        else:
            if (os.path.isdir(odir) == False):
                raise IOError("Specified output directory %s is a file" % odir)
        os.chdir(odir)

    return old_dir


def serialize_tiles(tile_list, strrefl, mask_list=None, strmask=None):
    """
    Serialises the tile

    :param tile_list: list of tiles to serialize
    :type tile_list: list of tiles, tile type as that returned by
                     Gridworkflow.list_tiles()
    :param strrefl: output filename for reflectance datasets
    :type strrefl: string
    :param mask_list: list of pq tiles to serialize
    :type mask_list: list of tiles
    :param strmask: output filename for pq datasets
    :type strmask: string
    """

    # serialize the tile
    with open(strrefl, 'wb') as fid:
        pickle.dump(tile_list, fid)

    if (strmask is not None):
        # serialize the mask
        with open(strmask, 'wb') as fid:
            pickle.dump(mask_list, fid)

    return


# raises ValueError if product not in Datacube product list


def query_dc(ul_latlon, lr_latlon, start_date, end_date, product,
             dc_config=None, sCRS='EPSG:4326'):
    """
    Returns a dict of tiles (single single spatial footprint, multiple dates)
    at resolution and CRS of the product.  Output grid is EPSG:4326

    :param ul_latlon: upper left coords
    :type ul_latlon: tuple float
    :param lr_latlon: lower right coords
    :type lr_latlon: tuple float
    :param start_date: start date for search range
    :type start_date: string
    :param end_date: end date for search
    :type end_date: string
    :param product: datacube product to search for
    :type product: string
    :param dcconf:
    :type dcconf: string?
    :param sCRS: coordinate reference system.Currently only supporting EPSG:4326
    :type sCRS: strin
    :rtype: dict[(int, int, numpy.datetime64), Tile], returns {} if with the
                given search criteria no datasets are found.  Same type as that
                returned by Gridworkflow.list_tiles()
    :raises: ValueError if product not in Datacube product list
    """
    # TODO: should at some stage expand code to handle user specified output
    # grid
    # NB: need to calculate tile_origin = (left,bottom) coord of bounding box
    #     need to calculate tile_size

    # CONNECT TO DATACUBE
    dc = datacube.Datacube(config=dc_config, app='dc_utils')

    # DOES PRODUCT EXIST?
    df_prods = dc.list_products()  # returns as panda dataframe
    bTest = product in df_prods['name'].tolist()
    if (bTest is False):
        raise ValueError("Specified product %s not found in datacube"
                         % product)

    # GET PRODUCT
    series_prod_X = df_prods[df_prods['name'] == product].squeeze()

    # PRODUCT PROPERTIES
    # (name, description, product_type, sat_path, format, lon, platform,
    #  sat_row, instrument, time, lat, crs, resolution, tile_size,
    # spatial_dimensions)

    oCRS = series_prod_X['crs']
    oRes = series_prod_X['resolution']

    # SEARCH AREA in Lat,Lons
    lat_tmp = [ul_latlon[0], lr_latlon[0]]
    lon_tmp = [ul_latlon[1], lr_latlon[1]]
    lat = (min(lat_tmp), max(lat_tmp))
    lon = (min(lon_tmp), max(lon_tmp))

    # CALCULATE TILE_SIZE --- will return single tile, multiple dates
    # at this point CRS, res, and tile_size are all in same units
    # lat long -> oCRS
    # (left,bottom,right,top)
    tmp = BoundingBox(lon[0], lat[0], lon[1], lat[1])
    # version change in API
    # igeopoly = GeoPolygon.from_boundingbox( tmp , crs=CRS(sCRS))
    igeopoly = _polygon_from_boundingbox(tmp, crs=CRS(sCRS))

    # Setup GeoBox for new output grid
    # resolution must be specified in (Y,X) order
    # oRes must be in this order (res_new_Y,res_new_X)
    geobox = GeoBox.from_geopolygon(igeopoly, oRes, crs=CRS(oCRS))

    output_grid_bbox = geobox.extent.boundingbox

    # Height and Width of new output grid in pixels
    # shape is (HEIGHT, WIDTH) ie (Y,X)
    height = geobox.height
    width = geobox.width

    # tile_size must be in (y,x) order, resolution (y,x)
    # order must be in CRS units, origin-Y,X
    # tile_size is in units of CRS ie m
    # resolution is the pixel size
    res_new_Y = abs(oRes[0])
    res_new_X = abs(oRes[1])
    oTile_size = (height*res_new_Y, width*res_new_X)

    # NEED TO SET ORIGIN for spatial foot print of new tile
    # origin-Y,X  - bottom left coord  **this key point in correcting bug
    oX = output_grid_bbox.left
    oY = output_grid_bbox.bottom

    oOrigin = (oY, oX)

    # SETUP OUTPUT GRID - SINGLE TILE with origin set to the origin of the
    # search area
    gs = GridSpec(crs=CRS(oCRS), tile_size=oTile_size,
                  resolution=oRes, origin=oOrigin)

    '''
    t00=gs.tile_geobox((0,0)).extent.boundingbox
    print 'Converting tile to geographic'
    print helper_func(t00)
    '''

    '''This is now working  - i.e. returning a single tile
    qdict = {'latitude': lat, 'longitude': lon,
             'time': (start_date, end_date) }
    tiles= gw.list_tiles(product=product, **qdict)
    '''
    gw = GridWorkflow(dc.index, grid_spec=gs, product=product)

    qdict = {'time': (start_date, end_date)}

    # dict[(int, int, numpy.datetime64), Tile]
    tiles = gw.list_tiles((0, 0), product=product, **qdict)

    # TODO provide option to cull dates which don't entirely encompass search
    # area...
    #     geopolygon = get_bounds(dta_list,CRS(crs))

    return tiles


def query_datacube(ul_latlon, lr_latlon, start_date, end_date, refl, pq=None,
                   dcconf=None, sCRS='EPSG:4326'):
    """
     Query the datacube.  Search for reflectance datasets and optionally find
     matching PQ datasets.

    :param ul_latlon: upper left coordinate
    :type ul_latlon:  tuple float
    :param lr_latlon: lower right coordinate
    :type lr_latlon: tuple float
    :param start_date: start date for search range
    :type start_date: string
    :param end_date: end date for search
    :type end_date: string
    :param refl: reflectance datacube product to search for
    :type refl: string
    :param pq: PQ datacube product to search for.
    :type pq: string
    :param dcconf:
    :type dcconf: string?
    :param sCRS: coordinate reference system.Currently only supporting EPSG:4326
    :type sCRS: string
    :return list of reflectance and PQ tiles and list of keys
    :rtype list of tiles, tile type as that returned by
            Gridworkflow.list_tiles()
    """

    refl_tiles = []
    pq_tiles = []
    tile_info = []

    # ValueError exception will be raised by query_dc if
    # product not found in database
    # returns a dictionary

    refl_tiles = query_dc(ul_latlon, lr_latlon, start_date, end_date, refl,
                          dc_config=dcconf, sCRS=sCRS)
    if (len(refl_tiles) == 0):
        return refl_tiles, pq_tiles, tile_info

    # convert to list and sort keys by date
    refl_keys = list(refl_tiles.keys())
    refl_keys.sort(key=lambda tup: tup[-1])
    refl_list = [refl_tiles[k] for k in refl_keys]

    # PQ list elements all set to None
    pq_list = [None] * len(refl_list)

    if (pq is not None):
        # ValueError exception will be raised by query_dc
        # if product not found in database
        pq_tiles = query_dc(ul_latlon, lr_latlon, start_date, end_date, pq,
                            dc_config=dcconf, sCRS=sCRS)
        pq_keys = list(pq_tiles.keys())
        # check if date of refl tile in pq_list
        # find matching dates, pairs of (refl,pq)
        # if refl date does not have matching pq then, then entry in pq_list
        # for that date is None
        for ix in range(len(refl_list)):
            if (refl_keys[ix] in pq_keys):
                pq_list[ix] = pq_tiles[refl_keys[ix]]

    tile_info = refl_keys

    return refl_list, pq_list, tile_info


def query_datacube_and_serialize_tiles(query, odir=None, outf_prefix=None,
                                       single=True):
    """
    Query the datacube and serialize (pickle) the returned tiles.

    :param query: query parameters
    :type query: dict
    :param odir: output directory for tiles
    :type odir: string
    :param outf_prefix: prefix to attach to file name
    :type outf_prefix: string
    :param single: true indicates all tiles serialized to same file as list
    :type single: bool
    """

    olddir = create_dir(odir)

    if (outf_prefix is None):
        outf_prefix = 'Tile'

    # ValueError exception will be raised by query_dc if product not
    # found in database
    tile_list, pq_list, tile_info = query_datacube(query['ul_latlon'],
                                                   query['lr_latlon'],
                                                   query['start_date'],
                                                   query['end_date'],
                                                   query['refl'],
                                                   pq=query['pq'],
                                                   dcconf=query['dcconf'],
                                                   sCRS='EPSG:4326')

    if (len(tile_list) == 0):
        return

    mask = None

    if (single is False):
        # multiple files

        ntiles = len(tile_list)
        strrefl_list = [None] * ntiles
        strmask_list = [None] * ntiles

        for ix in range(len(tile_list)-1):
            # setup output name prefix_sensor_date.pkl
            strdate = datetostring(tile_info[ix][-1])
            outf = outf_prefix + '_'+ strdate
            strrefl_list[ix] = outf+'_REFL.pkl'

            if (query['pq'] != None):
                mask = pq_list[ix]
                strmask_list[ix] = outf+'_PQ.pkl'

            serialize_tiles(tile_list[ix], strrefl_list[ix], mask_list=mask,
                            strmask=strmask_list[ix])

    else:
        # single file => pickle list of tiles

        strrefl_list = [None]
        strmask_list = [None]
        outf = outf_prefix + '_'+ datetostring(tile_info[0][-1]) + '_' + \
            datetostring(tile_info[-1][-1])
        strrefl_list[0] = outf+'_REFL.pkl'

        if (query['pq'] != None):
            mask = pq_list
            strmask_list[0] = outf+'_PQ.pkl'

        serialize_tiles(tile_list, strrefl_list[0], mask_list=mask,
                        strmask=strmask_list[0])

    os.chdir(olddir)

    return strrefl_list, strmask_list, tile_info


def query_datacube_main(argv):
    """
    Query the datacube and serialize (pickle) the returned tiles

    Usage:

    query_datacube.py -q <query>
                     -o <output dir*> -f <filename output prefix*>,
                     -z <multiple tiles*>

    *indicate optional

    :param argv: list of command line arguments as detailed below
    :type argv: string

    -q <query> - yaml file containing the query to be passed to GW.list_tiles()
    -o <ouput dir> - string specifying output directory for the tile data.
    -f <filename prefix> - string, with prefix to attach to output files
    -z - if present indicates that all tile data are to be written to a multiple
         files.

    """

    # currently not used in workflow
    # TODO: seems like -z behaviour inconsistent between modules
    um = ['query_datacube.py ',
          '-q <query> -o <output dir*> -f <filename output prefix*>\n',
          '                 -z <multiple tiles*>\n',
          '  Note options with * are optional']

    usage_message = ''.join(um)
    odir = None
    ouf_prefix = None
    single = True

    try:
        opts, args = getopt.getopt(argv, 'hq:o:f:z', ['query',
                                                      'odir',
                                                      'prefix',
                                                      'multi'])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)

    bMandatory = [False]
    for opt, arg in opts:
        if (opt == '-h'):
            print(usage_message)
            sys.exit(2)
        elif opt in ('-q', '--query'):
            # query
            try:
                query = load_query(arg)
            except Exception as e:
                print(e)
                sys.exit(2)
            query = load_query(arg)
            bMandatory[0] = True
        elif opt in ('-o', '--odir'):
            # directory to write tiles and job scripts
            odir = arg
        elif opt in ('-f', '--prefix'):
            # filename prefix for job scripts and tiles
            outf_prefix = arg
        elif opt in ('-z', '--multi'):
            # Output multiple files...one for each date or write tile list to
            # file
            single = False
        else:
            print('Invalid switch ' + opt)
            sys.exit(2)

    if (all(bMandatory) == False):
        print('Error missing command line argument ')
        print(usage_message)
        sys.exit(2)

    print('Processing Commenced')

    logging.debug(query)
    logging.debug(odir)
    logging.debug(outf_prefix)

    try:
        strrefl_list, strmask_list, tile_info = \
            query_datacube_and_serialize_tiles(query, odir=odir,
                                               outf_prefix=outf_prefix,
                                               single=single)
    except Exception as e:
        print ('Program failed with %s\n' % e)
        sys.exit(2)

    print('Processing complete')

    return


def main():

    query_datacube_main(sys.argv[1:])

    return


if __name__ == "__main__":

    query_datacube_main(sys.argv[1:])
