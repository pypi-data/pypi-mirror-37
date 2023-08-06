'''
Created on 18May,2017

@author: cac009
'''
import multiprocessing as mp
import copy
import sambuca as sb
from swampy.sen2coral.sambuca_calculations import sam_com
import logging
import numpy as np
import time
import sys

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def cp_sub_into_main_rr(rr_main, rr_sub, ys=None ,ye=None):
    """
    Copies subset of results recorder into main results recorder

    :param rr_main:
    :type rr_main:
    :param rr_sub:
    :type rr_sub:
    :param ys:
    :type ys:
    :param ye:
    :type ye:
    """

    rr_main.error_alpha[ys:ye,:] = rr_sub.error_alpha
    rr_main.error_alpha_f[ys:ye,:] = rr_sub.error_alpha_f
    rr_main.error_f[ys:ye,:] = rr_sub.error_f
    rr_main.error_lsq[ys:ye,:] = rr_sub.error_lsq
    rr_main.chl[ys:ye,:] = rr_sub.chl
    rr_main.cdom[ys:ye,:] = rr_sub.cdom
    rr_main.nap[ys:ye,:] = rr_sub.nap
    rr_main.depth[ys:ye,:] = rr_sub.depth
    rr_main.sub1_frac[ys:ye,:] = rr_sub.sub1_frac
    rr_main.sub2_frac[ys:ye,:] = rr_sub.sub2_frac
    rr_main.sub3_frac[ys:ye,:] = rr_sub.sub3_frac
    rr_main.closed_rrs[ys:ye,:,:] = rr_sub.closed_rrs
    rr_main.nit[ys:ye,:] = rr_sub.nit
    rr_main.success[ys:ye,:] = rr_sub.success
    rr_main.kd[ys:ye,:] = rr_sub.kd
    rr_main.sdi[ys:ye,:] = rr_sub.sdi

    return


def sam_com_mp(observed_rrs, objective, siop, result_recorder, image_info,
                mask=None, shallow = False, method='SLSQP', maxit=500,
                pool=None):
    """
    Computes SWAMpy on reflectance image. Uses multiprocessing module to process
    spatial tiles in parallel.

    :param observed_rrs: refl dataset on which to perform SWAMpy calculation
    :type observed_rrs: 3d numpy array (bands,rows,cols)
    :param objective: objective function for minimization
    :type objective: class SciPyObjective(Callable) see sambuca for details
    :param siop: contain siop datasets loaded into memory
    :type siop: dict
    :param results_recorder: SWAMpy results for image
    :type results_recorder: class ArrayResultWriter see Sambuca documentation
    :param image_info: image info metadata ncols, nrows etc
    :type image_info: dict
    :param mask: mask used to constrain SWAMpy calculation only to valid pixels
    :type mask: 2d numpy array
    :param shallow:
    :type shallow: bool
    :param method: optimization algorithm
    :type method: string
    :param maxit: number of iteration of the optimization routine to perform
    :type maxit: int
    :param pool: # number of parallel processes
    :type pool: int
    :return rr_main results of SWAMpy calculation
    :rtype  class ArrayResultWriter see Sambuca documentation
    """

    if (pool is None):
        nprocs = mp.cpu_count()
    else:
        nprocs = pool

    logging.debug(nprocs)

    jobs = []

    height = image_info['observed_rrs_height']
    width = image_info['observed_rrs_width']
    rr_main = result_recorder
    sensor_filter = rr_main._sensor_filter
    nedr =  rr_main._nedr
    fx_param = rr_main._fixed_parameters

    # setup tiling...lines of data
    tile_ny =  int(height / nprocs)
    tile_ny = 1
    ysA = np.arange(0, height, tile_ny)
    yeA = np.roll(ysA,-1)
    yeA[-1] = height
    tiles = zip(ysA, yeA)

    logging.debug(tiles)

    pp = mp.Pool(processes=nprocs)

    #print(nprocs)

    t0 = time.time()

    # doubling the amount of memory required for input and output
    for ys, ye in tiles:

        # copy objective function...concern over side effects
        objf = copy.copy(objective)
        i_info = copy.copy(image_info)
        i_info['observed_rrs_height'] = ye-ys
        # create sub section of the results recorder
        rr = sb.ArrayResultWriter(ye-ys, width, sensor_filter, nedr, fx_param)

        args = (observed_rrs[:,ys:ye,:], objf, siop, rr, i_info)
        if (mask is not None):
            tmpMask = mask[ys:ye,:]
        else:
            tmpMask = None
        kwargs = {'mask': tmpMask, 'shallow': shallow, 'maxit': maxit}

        # TODO: improve load balancing
        jobs.append(pp.apply_async(sam_com, args, kwargs))

    tile_list = list(tiles) # tiles will be an empty object after this call

    npix_sum = 0
    njobs = len(jobs)
    ttsum = 0.0
    for j in range(njobs):
        # get result of process

        rr, coords, npix, tt, tpx  = jobs[j].get()
        npix_sum = npix_sum + npix
        # Copy results into results recorder
        cp_sub_into_main_rr(rr_main, rr, ys=ysA[j] ,ye=yeA[j])

        ttsum = ttsum + tt
        j1 = j + 1
        eta = float(njobs - j1) * (ttsum / j1) / nprocs / 60.0
        suffix = '[Last line: total {:.4f}s/ Per pix {:.4f}s, Line {} of {}, ETA {:.2f} min]' \
                .format(tt, tpx, j, njobs, eta)
        progress(j, njobs, suffix=suffix)


    pp.close()

    t1 = time.time()

    coords = [0, height-1, 0, width-1]

    print("\nTotal execution time: {0:.1f} seconds".format(t1-t0))
    print("Average time per pixel: {0:.3f} seconds".format((t1-t0)/(height*width)))

    return rr_main, coords, npix_sum
