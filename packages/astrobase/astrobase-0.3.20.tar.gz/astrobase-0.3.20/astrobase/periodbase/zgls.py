#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''zgls.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Jan 2017

Contains the Zechmeister & Kurster (2002) Generalized Lomb-Scargle period-search
algorithm implementation for periodbase.

'''

#############
## LOGGING ##
#############

import logging
from datetime import datetime
from traceback import format_exc

# setup a logger
LOGGER = None
LOGMOD = __name__
DEBUG = False

def set_logger_parent(parent_name):
    globals()['LOGGER'] = logging.getLogger('%s.%s' % (parent_name, LOGMOD))

def LOGDEBUG(message):
    if LOGGER:
        LOGGER.debug(message)
    elif DEBUG:
        print('[%s - DBUG] %s' % (
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            message)
        )

def LOGINFO(message):
    if LOGGER:
        LOGGER.info(message)
    else:
        print('[%s - INFO] %s' % (
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            message)
        )

def LOGERROR(message):
    if LOGGER:
        LOGGER.error(message)
    else:
        print('[%s - ERR!] %s' % (
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            message)
        )

def LOGWARNING(message):
    if LOGGER:
        LOGGER.warning(message)
    else:
        print('[%s - WRN!] %s' % (
            datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            message)
        )

def LOGEXCEPTION(message):
    if LOGGER:
        LOGGER.exception(message)
    else:
        print(
            '[%s - EXC!] %s\nexception was: %s' % (
                datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                message, format_exc()
            )
        )


#############
## IMPORTS ##
#############

from multiprocessing import Pool, cpu_count
import numpy as np

# import these to avoid lookup overhead
from numpy import nan as npnan, sum as npsum, abs as npabs, \
    roll as nproll, isfinite as npisfinite, std as npstd, \
    sign as npsign, sqrt as npsqrt, median as npmedian, \
    array as nparray, percentile as nppercentile, \
    polyfit as nppolyfit, var as npvar, max as npmax, min as npmin, \
    log10 as nplog10, arange as nparange, pi as MPI, floor as npfloor, \
    argsort as npargsort, cos as npcos, sin as npsin, tan as nptan, \
    where as npwhere, linspace as nplinspace, \
    zeros_like as npzeros_like, full_like as npfull_like, \
    arctan as nparctan, nanargmax as npnanargmax, nanargmin as npnanargmin, \
    empty as npempty, ceil as npceil, mean as npmean, \
    digitize as npdigitize, unique as npunique, \
    argmax as npargmax, argmin as npargmin, zeros as npzeros, nanmax as npnanmax


###################
## LOCAL IMPORTS ##
###################

from ..lcmath import phase_magseries, sigclip_magseries, time_bin_magseries, \
    phase_bin_magseries

from . import get_frequency_grid


############
## CONFIG ##
############

NCPUS = cpu_count()


######################################################
## PERIODOGRAM VALUE EXPRESSIONS FOR A SINGLE OMEGA ##
######################################################

def generalized_lsp_value(times, mags, errs, omega):
    '''Generalized LSP value for a single omega.

    P(w) = (1/YY) * (YC*YC/CC + YS*YS/SS)

    where: YC, YS, CC, and SS are all calculated at T

    and where: tan 2omegaT = 2*CS/(CC - SS)

    and where:

    Y = sum( w_i*y_i )
    C = sum( w_i*cos(wT_i) )
    S = sum( w_i*sin(wT_i) )

    YY = sum( w_i*y_i*y_i ) - Y*Y
    YC = sum( w_i*y_i*cos(wT_i) ) - Y*C
    YS = sum( w_i*y_i*sin(wT_i) ) - Y*S

    CpC = sum( w_i*cos(w_T_i)*cos(w_T_i) )
    CC = CpC - C*C
    SS = (1 - CpC) - S*S
    CS = sum( w_i*cos(w_T_i)*sin(w_T_i) ) - C*S

    '''

    one_over_errs2 = 1.0/(errs*errs)

    W = npsum(one_over_errs2)
    wi = one_over_errs2/W

    sin_omegat = npsin(omega*times)
    cos_omegat = npcos(omega*times)

    sin2_omegat = sin_omegat*sin_omegat
    cos2_omegat = cos_omegat*cos_omegat
    sincos_omegat = sin_omegat*cos_omegat

    # calculate some more sums and terms
    Y = npsum( wi*mags )
    C = npsum( wi*cos_omegat )
    S = npsum( wi*sin_omegat )

    YpY = npsum( wi*mags*mags)

    YpC = npsum( wi*mags*cos_omegat )
    YpS = npsum( wi*mags*sin_omegat )

    CpC = npsum( wi*cos2_omegat )
    # SpS = npsum( wi*sin2_omegat )

    CpS = npsum( wi*sincos_omegat )

    # the final terms
    YY = YpY - Y*Y
    YC = YpC - Y*C
    YS = YpS - Y*S
    CC = CpC - C*C
    SS = 1 - CpC - S*S  # use SpS = 1 - CpC
    CS = CpS - C*S

    # calculate tau
    tan_omega_tau_top = 2.0*CS
    tan_omega_tau_bottom = CC - SS
    tan_omega_tau = tan_omega_tau_top/tan_omega_tau_bottom
    tau = nparctan(tan_omega_tau/(2.0*omega))

    periodogramvalue = (YC*YC/CC + YS*YS/SS)/YY

    return periodogramvalue



def generalized_lsp_value_notau(times, mags, errs, omega):
    '''
    This is the simplified version not using tau.

    W = sum (1.0/(errs*errs) )
    w_i = (1/W)*(1/(errs*errs))

    Y = sum( w_i*y_i )
    C = sum( w_i*cos(wt_i) )
    S = sum( w_i*sin(wt_i) )

    YY = sum( w_i*y_i*y_i ) - Y*Y
    YC = sum( w_i*y_i*cos(wt_i) ) - Y*C
    YS = sum( w_i*y_i*sin(wt_i) ) - Y*S

    CpC = sum( w_i*cos(w_t_i)*cos(w_t_i) )
    CC = CpC - C*C
    SS = (1 - CpC) - S*S
    CS = sum( w_i*cos(w_t_i)*sin(w_t_i) ) - C*S

    D(omega) = CC*SS - CS*CS
    P(omega) = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*D)

    '''

    one_over_errs2 = 1.0/(errs*errs)

    W = npsum(one_over_errs2)
    wi = one_over_errs2/W

    sin_omegat = npsin(omega*times)
    cos_omegat = npcos(omega*times)

    sin2_omegat = sin_omegat*sin_omegat
    cos2_omegat = cos_omegat*cos_omegat
    sincos_omegat = sin_omegat*cos_omegat

    # calculate some more sums and terms
    Y = npsum( wi*mags )
    C = npsum( wi*cos_omegat )
    S = npsum( wi*sin_omegat )

    YpY = npsum( wi*mags*mags)

    YpC = npsum( wi*mags*cos_omegat )
    YpS = npsum( wi*mags*sin_omegat )

    CpC = npsum( wi*cos2_omegat )
    # SpS = npsum( wi*sin2_omegat )

    CpS = npsum( wi*sincos_omegat )

    # the final terms
    YY = YpY - Y*Y
    YC = YpC - Y*C
    YS = YpS - Y*S
    CC = CpC - C*C
    SS = 1 - CpC - S*S  # use SpS = 1 - CpC
    CS = CpS - C*S

    # P(omega) = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*D)
    # D(omega) = CC*SS - CS*CS
    Domega = CC*SS - CS*CS
    lspval = (SS*YC*YC + CC*YS*YS - 2.0*CS*YC*YS)/(YY*Domega)

    return lspval



def specwindow_lsp_value(times, mags, errs, omega):
    '''
    This calculates the peak associated with the spectral window function
    for times and at the specified omega.

    '''

    norm_times = times - times.min()

    tau = (
        (1.0/(2.0*omega)) *
        nparctan( npsum(npsin(2.0*omega*norm_times)) /
                  npsum(npcos(2.0*omega*norm_times)) )
    )

    lspval_top_cos = (npsum(1.0 * npcos(omega*(norm_times-tau))) *
                      npsum(1.0 * npcos(omega*(norm_times-tau))))
    lspval_bot_cos = npsum( (npcos(omega*(norm_times-tau))) *
                            (npcos(omega*(norm_times-tau))) )

    lspval_top_sin = (npsum(1.0 * npsin(omega*(norm_times-tau))) *
                      npsum(1.0 * npsin(omega*(norm_times-tau))))
    lspval_bot_sin = npsum( (npsin(omega*(norm_times-tau))) *
                            (npsin(omega*(norm_times-tau))) )

    lspval = 0.5 * ( (lspval_top_cos/lspval_bot_cos) +
                     (lspval_top_sin/lspval_bot_sin) )

    return lspval


##############################
## GENERALIZED LOMB-SCARGLE ##
##############################

def glsp_worker(task):
    '''This is a worker to wrap the generalized Lomb-Scargle single-frequency
    function.

    '''

    try:
        return generalized_lsp_value(*task)
    except Exception as e:
        return npnan



def glsp_worker_specwindow(task):
    '''This is a worker to wrap the generalized Lomb-Scargle single-frequency
    function.

    '''

    try:
        return specwindow_lsp_value(*task)
    except Exception as e:
        return npnan



def glsp_worker_notau(task):
    '''This is a worker to wrap the generalized Lomb-Scargle single-freq func.

    This version doesn't use tau.

    '''

    try:
        return generalized_lsp_value_notau(*task)
    except Exception as e:
        return npnan



def pgen_lsp(
        times,
        mags,
        errs,
        magsarefluxes=False,
        startp=None,
        endp=None,
        autofreq=True,
        nbestpeaks=5,
        periodepsilon=0.1,
        stepsize=1.0e-4,
        nworkers=None,
        workchunksize=None,
        sigclip=10.0,
        glspfunc=glsp_worker,
        verbose=True
):
    '''This calculates the generalized LSP given times, mags, errors.

    Uses the algorithm from Zechmeister and Kurster (2009). By default, this
    calculates a frequency grid to use automatically, based on the autofrequency
    function from astropy.stats.lombscargle. If startp and endp are provided,
    will generate a frequency grid based on these instead.

    '''

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # get rid of zero errs
    nzind = np.nonzero(serrs)
    stimes, smags, serrs = stimes[nzind], smags[nzind], serrs[nzind]


    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        # get the frequencies to use
        if startp:
            endf = 1.0/startp
        else:
            # default start period is 0.1 day
            endf = 1.0/0.1

        if endp:
            startf = 1.0/endp
        else:
            # default end period is length of time series
            startf = 1.0/(stimes.max() - stimes.min())

        # if we're not using autofreq, then use the provided frequencies
        if not autofreq:
            omegas = 2*np.pi*np.arange(startf, endf, stepsize)
            if verbose:
                LOGINFO(
                    'using %s frequency points, start P = %.3f, end P = %.3f' %
                    (omegas.size, 1.0/endf, 1.0/startf)
                )
        else:
            # this gets an automatic grid of frequencies to use
            freqs = get_frequency_grid(stimes,
                                       minfreq=startf,
                                       maxfreq=endf)
            omegas = 2*np.pi*freqs
            if verbose:
                LOGINFO(
                    'using autofreq with %s frequency points, '
                    'start P = %.3f, end P = %.3f' %
                    (omegas.size, 1.0/freqs.max(), 1.0/freqs.min())
                )

        # map to parallel workers
        if (not nworkers) or (nworkers > NCPUS):
            nworkers = NCPUS
            if verbose:
                LOGINFO('using %s workers...' % nworkers)

        pool = Pool(nworkers)

        tasks = [(stimes, smags, serrs, x) for x in omegas]
        if workchunksize:
            lsp = pool.map(glspfunc, tasks, chunksize=workchunksize)
        else:
            lsp = pool.map(glspfunc, tasks)

        pool.close()
        pool.join()
        del pool

        lsp = np.array(lsp)
        periods = 2.0*np.pi/omegas

        # find the nbestpeaks for the periodogram: 1. sort the lsp array by
        # highest value first 2. go down the values until we find five
        # values that are separated by at least periodepsilon in period

        # make sure to filter out non-finite values of lsp

        finitepeakind = npisfinite(lsp)
        finlsp = lsp[finitepeakind]
        finperiods = periods[finitepeakind]

        # make sure that finlsp has finite values before we work on it
        try:

            bestperiodind = npargmax(finlsp)

        except ValueError:

            LOGERROR('no finite periodogram values '
                     'for this mag series, skipping...')
            return {'bestperiod':npnan,
                    'bestlspval':npnan,
                    'nbestpeaks':nbestpeaks,
                    'nbestlspvals':None,
                    'nbestperiods':None,
                    'lspvals':None,
                    'omegas':omegas,
                    'periods':None,
                    'method':'gls',
                    'kwargs':{'startp':startp,
                              'endp':endp,
                              'stepsize':stepsize,
                              'autofreq':autofreq,
                              'periodepsilon':periodepsilon,
                              'nbestpeaks':nbestpeaks,
                              'sigclip':sigclip}}

        sortedlspind = np.argsort(finlsp)[::-1]
        sortedlspperiods = finperiods[sortedlspind]
        sortedlspvals = finlsp[sortedlspind]

        prevbestlspval = sortedlspvals[0]

        # now get the nbestpeaks
        nbestperiods, nbestlspvals, peakcount = (
            [finperiods[bestperiodind]],
            [finlsp[bestperiodind]],
            1
        )
        prevperiod = sortedlspperiods[0]

        # find the best nbestpeaks in the lsp and their periods
        for period, lspval in zip(sortedlspperiods, sortedlspvals):

            if peakcount == nbestpeaks:
                break
            perioddiff = abs(period - prevperiod)
            bestperiodsdiff = [abs(period - x) for x in nbestperiods]

            # print('prevperiod = %s, thisperiod = %s, '
            #       'perioddiff = %s, peakcount = %s' %
            #       (prevperiod, period, perioddiff, peakcount))

            # this ensures that this period is different from the last
            # period and from all the other existing best periods by
            # periodepsilon to make sure we jump to an entire different peak
            # in the periodogram
            if (perioddiff > (periodepsilon*prevperiod) and
                all(x > (periodepsilon*prevperiod) for x in bestperiodsdiff)):
                nbestperiods.append(period)
                nbestlspvals.append(lspval)
                peakcount = peakcount + 1

            prevperiod = period


        return {'bestperiod':finperiods[bestperiodind],
                'bestlspval':finlsp[bestperiodind],
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':nbestlspvals,
                'nbestperiods':nbestperiods,
                'lspvals':lsp,
                'omegas':omegas,
                'periods':periods,
                'method':'gls',
                'kwargs':{'startp':startp,
                          'endp':endp,
                          'stepsize':stepsize,
                          'autofreq':autofreq,
                          'periodepsilon':periodepsilon,
                          'nbestpeaks':nbestpeaks,
                          'sigclip':sigclip}}

    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return {'bestperiod':npnan,
                'bestlspval':npnan,
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':None,
                'nbestperiods':None,
                'lspvals':None,
                'omegas':None,
                'periods':None,
                'method':'gls',
                'kwargs':{'startp':startp,
                          'endp':endp,
                          'stepsize':stepsize,
                          'autofreq':autofreq,
                          'periodepsilon':periodepsilon,
                          'nbestpeaks':nbestpeaks,
                          'sigclip':sigclip}}



def specwindow_lsp(
        times,
        mags,
        errs,
        magsarefluxes=False,
        startp=None,
        endp=None,
        autofreq=True,
        nbestpeaks=5,
        periodepsilon=0.1,
        stepsize=1.0e-4,
        nworkers=None,
        sigclip=10.0,
        glspfunc=glsp_worker_specwindow,
        verbose=True
):
    '''
    This calculates the spectral window function.

    '''

    # run the LSP using glsp_worker_specwindow as the worker
    lspres = pgen_lsp(
        times,
        mags,
        errs,
        magsarefluxes=magsarefluxes,
        startp=startp,
        endp=endp,
        autofreq=autofreq,
        nbestpeaks=nbestpeaks,
        periodepsilon=periodepsilon,
        stepsize=stepsize,
        nworkers=nworkers,
        sigclip=sigclip,
        glspfunc=glsp_worker_specwindow,
        verbose=verbose
    )

    # update the resultdict to indicate we're a spectral window function
    lspres['method'] = 'win'

    if lspres['lspvals'] is not None:

        # renormalize the periodogram to between 0 and 1 like the usual GLS.
        lspmax = npnanmax(lspres['lspvals'])

        if np.isfinite(lspmax):

            lspres['lspvals'] = lspres['lspvals']/lspmax
            lspres['nbestlspvals'] = [
                x/lspmax for x in lspres['nbestlspvals']
            ]
            lspres['bestlspval'] = lspres['bestlspval']/lspmax

    return lspres
