'''
Created on 22May,2017

@author: cac009
'''
#%matplotlib inline
#%matplotlib inline
import datacube
import logging
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import pandas as pd
import xarray as xr

import click
from datacube.api import GridWorkflow
import glob
import pickle


def unpickle_tile(inf):

    with open(inf, 'rb') as fid:
        itile = pickle.load(fid)

    return itile


#class StrListParamType(click.ParamType):
#    name='list'

#    def convert(self, value, param, ctx):
#        try:
#            return eval(value)
#        except ValueError:
#            self.fail('{0} {1} {2}'.format(value, param, ctx))


@click.command(help='Generates quick look images of Datacube tiles' +
    "\n\nGenerates quick look image of Datacube tiles" +
    "\n  Usage: tile_quicklooks *.pkl quicklook.png")
@click.argument('tilelist', type=click.Path(exists=True),
    nargs=-1)
@click.argument('outputfile', type=click.Path())
@click.option('--ncols', '-nc', type=int, default=3,
        help='number of plots per row in output image')
@click.option('--fsizex', '-fsx', type=float, default=10.0,
        help='figure size x-dim in inches')
@click.option('--dpi', '-dpi', type=int, default=80, help='dots per inch')
@click.option('--unpickle', '-unpkl', type=bool, default=True, help='unpickle tiles')
#@click.option('--bands', '-b', type=StrListParamType(), default="['blue', 'green', 'red']",
#    help='list of bands to display')
def tile_quicklooks(tilelist, outputfile, ncols=3, fsizex=10, dpi=80, unpickle=True):
#        bands=['blue', 'green', 'red']):
    """
    Given a list of reflectance datasets create a matrix of RGB true colour
    image plots.  Called from the command line

    """
    outf = outputfile
    tile_list = tilelist
    bands = ['blue', 'green', 'red']

    if (unpickle):
        refl_xr = GridWorkflow.load(unpickle_tile(tile_list[0]), measurements=bands)
    else:
        refl_xr = GridWorkflow.load(tile_list[0], measurements=bands)

    nt = len(tile_list)
    nx_i = refl_xr.dims['x']
    ny_i = refl_xr.dims['y']
    xsize = fsizex*dpi
    nrows = math.ceil(nt / ncols)
    nx_p = xsize / ncols
    scale = int(np.ceil(nx_i / nx_p))
    fsizey = ny_i / scale * nrows / dpi
    fsize = (fsizex,fsizey)
    #print(fsize)
    fig = plt.figure(figsize = fsize, dpi=dpi)
    date_list = refl_xr.coords['time'].values
    ip = 1
    for itile in tile_list:

        if (unpickle):
            refl_xr = GridWorkflow.load(unpickle_tile(itile), measurements=bands)
        else:
            refl_xr = GridWorkflow.load(itile, measurements=bands)

        idate = refl_xr.coords['time'].values

        ob = refl_xr.isel(time=[0])

        b = ob.blue.squeeze(dim='time').values

        b = b[0:-1:scale, 0:-1:scale]
        g = ob.green.squeeze(dim='time').values
        g = g[0:-1:scale, 0:-1:scale]
        r = ob.red.squeeze(dim='time').values
        r = r[0:-1:scale, 0:-1:scale]

        r[r < 0] = 0
        r[r > 3000] = 3000
        g[g < 0] = 0
        g[g > 3000] = 3000
        b[b < 0] = 0
        b[b > 3000] = 3000

        a = fig.add_subplot(nrows,ncols,ip)
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)

        date = pd.to_datetime(idate[0])
        strdate = date.strftime('%Y-%m-%d')
        a.set_title(strdate)

        rgb = np.stack([r,g,b], axis=2)

        rgb = rgb.astype('float32') / 3000.0

        imgplot = plt.imshow(rgb)

        ip = ip + 1

    fig.savefig(outf)

    return


def do_plot(refl_xr, ncols=3, fsize=(10,10), dpi=80):
    """
    Given a list of reflectance datasets create a matrix of RGB true colour
    image plots.  Called from iPython Notebooks

    :param refl_xr: reflectance datasets to plot. Must have blue, green, red
                    values
    :type refl_xr: xarray dataset as returned by Datacube.load() function
    :param ncols: number of images to be displayed in a row
    :type ncols: int
    :param fsize: figure size (width, height) in inches
    :type fsize: tuple float
    :param dpi: dpi of output image
    :type dpi: float
    """

    nt = refl_xr.dims['time']
    nx_i = refl_xr.dims['x']
    xsize = fsize[0]*dpi
    nrows = math.ceil(nt / ncols)
    nx_p = xsize / ncols
    scale = int(np.ceil(nx_i / nx_p))
    fig = plt.figure(figsize = fsize, dpi=dpi)
    date_list = refl_xr.coords['time'].values
    ip = 1
    for idate in date_list:

        ob = refl_xr.sel(time=idate)

        b = ob.blue.values

        b = b[0:-1:scale, 0:-1:scale]
        g = ob.green.values
        g = g[0:-1:scale, 0:-1:scale]
        r = ob.red.values
        r = r[0:-1:scale, 0:-1:scale]

        r[r < 0] = 0
        r[r > 3000] = 3000
        g[g < 0] = 0
        g[g > 3000] = 3000
        b[b < 0] = 0
        b[b > 3000] = 3000

        a = fig.add_subplot(nrows,ncols,ip)
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)

        date = pd.to_datetime(idate)
        strdate = date.strftime('%Y-%m-%d')
        a.set_title(strdate)

        rgb = np.stack([r,g,b], axis=2)

        rgb = rgb.astype('float32') / 3000.0

        imgplot = plt.imshow(rgb)

        ip = ip + 1

    fig.show()

    return


def do_plot_swampy_single_result(out_xr, ncols=3, fsize=(10,20), dpi=150):
    """
    Given an xarray dataset create a matrix of pseudo colour image plots, one
    for each variable.  Used to plot the outputs of SWAMpy.  Called from
    iPython notebook

    :param out_xr: xarray dataset to plot
    :type out_xr: xarray dataset with 2D variables
    :param ncols: number of images to be displayed in a row
    :type ncols: int
    :param fsize: figure size (width, height) in inches
    :type fsize: tuple float
    :param dpi: dpi of output image
    :type dpi: float
    """

    nt = len(out_xr.data_vars.keys())
    nx_i = out_xr.dims['x']
    xsize = fsize[0]*dpi
    nrows = math.ceil(nt / ncols)
    nx_p = xsize / ncols
    scale = int(np.ceil(nx_i / nx_p))
    fig = plt.figure(figsize = fsize, dpi=dpi)

    ip = 1

    for ikey in out_xr.data_vars.keys():

        if (ikey not in ['closed_rrs']):
            da = out_xr[ikey].squeeze(dim='time').values

            da = da[0:-1:scale, 0:-1:scale]

            da[da < 0.0] = 0.0

            a = fig.add_subplot(nrows,ncols,ip)
            a.xaxis.set_visible(False)
            a.yaxis.set_visible(False)
            a.set_title(ikey)
            imgplot = plt.imshow(da,cmap='rainbow')
            plt.colorbar()

            ip = ip + 1

        else:
            print('code for closed rrs')

    return


if __name__ == '__main__':

#     dc = datacube.Datacube()
#     ul_latlon = (-32.5,115.5)
#     lr_latlon = (-33.5,117.0)
#     query = {
#         'product': 'ls7_nbar_albers',
#         'time': ('2000-01-01', '2000-03-01'),
#         'lat': (-32.88,-33.5),
#         'lon': (115.5,116.0)
#     }
#
#     query = {
#         'product': 'ls7_nbar_albers',
#         'time': ('2000-01-01', '2000-02-01'),
#         'lat': (-32.88,-33.5),
#         'lon': (115.5,116.0),
#         'group_by': 'solar_day'
#     }
#
#     query = {
#         'product': 'ls7_nbar_albers',
#         'time': ('2000-01-01', '2000-12-01'),
#         'lat': (-32.5,-33.5),
#         'lon': (115.5,117.0),
#         'group_by': 'solar_day'
#     }

    print('do query')
#    refl_xr = dc.load( measurements=['blue','green','red','nir'], **query )
#    dim = refl_xr.dims

#    do_plot(refl_xr)

    # Test code for plotting SWAMpy results

    # filename='c:/Results/Landsat7_2000-02-27_SAMBUCAV2__inputs.nc'
#    filename='c:/Results/Landsat7_2000-02-27_SAMBUCAV2_.nc'
#    dt = xr.open_dataset(filename)

#    do_plot_swampy_single_result(dt.isel(time=0))

