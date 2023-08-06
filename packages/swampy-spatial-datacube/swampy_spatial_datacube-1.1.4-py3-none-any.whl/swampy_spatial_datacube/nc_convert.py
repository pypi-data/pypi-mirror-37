import os
import numpy as np
import xarray as xr
import click

import gdal
import gdalnumeric
import pandas as pd

#Assumes image is (nb,nl,ns) which is the case if LoadArray is used to read in image
def pyWriteImage(image, strfout,  gdal_format='ENVI', format_opts=None, metaData=None,
                 geotrans=None, proj=None, nval=None):# gdal_format='GTiff', format_opts=['COMPRESS=LZW']):

    gdal.UseExceptions()

    dim=image.shape
    nd=len(dim)
    if nd == 3:
        nb=dim[0]
        ny=dim[1]
        nx=dim[2]
    else:
        nb=1
        ny=dim[0]
        nx=dim[1]

    gdal_dt = gdalnumeric.GDALTypeCodeToNumericTypeCode(image.dtype.type)

    gdal_driver = gdal.GetDriverByName(gdal_format)


    if (format_opts !=None):
        output_dataset = gdal_driver.Create(strfout, nx, ny, nb, gdal_dt, format_opts)
    else:
        output_dataset = gdal_driver.Create(strfout, nx, ny, nb, gdal_dt)
    assert output_dataset, 'Unable to open output dataset %s'% output_dataset

    if (geotrans != None):
        output_dataset.SetGeoTransform(geotrans)
    if (proj != None):
        output_dataset.SetProjection(proj)

    if nd == 2:
        output_band = output_dataset.GetRasterBand(1)
        output_band.WriteArray(image[:,:])
        if (nval != None):
            if (nval[0] != None):
                output_band.SetNoDataValue(nval[0])
        output_band = None

    else:
        for ib in range(nb):
            output_band = output_dataset.GetRasterBand(ib+1)
            output_band.WriteArray(image[ib,:,:],0,0)
            #print ib
            if (nval != None):
                if (nval[ib] != None):
                    output_band.SetNoDataValue(nval[ib]) #assume this is the same type as dataype of image
            output_band =None

    #Copy metadata to output dataset
    if (metaData != None):
        ok=pySetMetaData(output_dataset, metaData)

    return True, output_dataset


def write_txt_descriptor(outf, bands, origin, pix_size, datum):

    with open(outf, "w") as f:
        f.write("Bands: {0}\n".format(str(bands)))
        f.write("Origin (0,0) pixel: ({0}, {1})\n".format(origin[0], origin[1]))
        f.write("Pixel size: ({0}, {1})\n".format(pix_size[0], pix_size[1]))
        f.write('Datum: {0}\n'.format(datum))

    return


@click.command(help='Convert SWAMpy netCDF file to other raster formats' +
    "\n\nConvert SWAMpy netCDF file to other raster formats")
@click.argument('ncfiles', type=click.Path(exists=True), nargs=-1)
@click.option('--split_on_date', '-sod', type=bool, default=True,
    help='Save all SWAMpy outputs for a single date in a single file')
@click.option('--gdal_format', '-of', type=str, default='ENVI',
    help='Output format as specified by a GDAL format code, default is "ENVI" ')
def nc_convert(ncfiles, split_on_date=True, gdal_format='ENVI'):

    bands = ['cdom', 'chl', 'nap', 'depth', 'sub1_frac', 'sub2_frac', 'sub3_frac',
            'sub1_frac_norm',  'sub2_frac_norm', 'sub3_frac_norm',
            'total_abun',
            'error_lsq', 'error_alpha', 'error_alpha_f', 'error_f',
            'success', 'kd',  'nit', 'sdi']
    nbands = len(bands)

    for inf in ncfiles:

        dt = xr.open_dataset(inf)
        # get number of dates in the netcdf
        dates = dt.time.values
        ndt = len(dates)

        datum = dt.attrs['crs']
        origin = (dt.x[0].values, dt.y[0].values)
        pix_size = (dt.x[1].values-dt.x[0].values, dt.y[1].values-dt.y[0].values)

        #dt_var = sorted(list(dict(dt.data_vars).keys())
        filename, file_ext = os.path.splitext(inf)

        dt_vars = list(dt.data_vars)
        if (all(x in dt_vars for x in bands) == False):
            print('Skipping {}\n'.format(inf))
            continue

        if (split_on_date):
            for idate in range(ndt):
                dta = dt[bands].isel(time=[idate]).to_array().squeeze(dim='time').values.astype(np.float32)
                date = pd.to_datetime(dates[idate])
                strdate = date.strftime('%Y-%m-%d')
                outf = filename + '_' + strdate
                ok, outfile = pyWriteImage(dta, outf,  gdal_format=gdal_format)
                outf = outf + '.txt'
                # write bands, write coordinate pixel, write datum
                write_txt_descriptor(outf, bands, origin, pix_size, datum)
        else:
            # implies split on product
            for iband in range(nbands):
                dta = dt[bands[iband]].values.astype(np.float32)
                outf = filename + '_' + bands[iband]
                ok, outfile = pyWriteImage(dta, outf,  gdal_format=gdal_format)
                outf = outf + '.txt'
                # write bands, write coordinate pixel, write datum
                write_txt_descriptor(outf, bands, origin, pix_size, datum)

    return


if __name__ == '__main__':

    inf = '/home/ubuntu/swampy-data-cfg-tiles/results/gbrLandsat8_GBR_2013-08-05_SWAMPYV2.nc'

    nc_convert(inf, split_on_date=True, gdal_format='ERS')





