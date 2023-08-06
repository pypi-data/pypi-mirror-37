#!/usr/bin/env python

'''kbls.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Jan 2017

Contains the Kovacs, et al. (2002) Box-Least-squared-Search period-search
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

from math import fmod

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
    argmax as npargmax, argmin as npargmin


###################
## LOCAL IMPORTS ##
###################

from ..lcmath import phase_magseries, sigclip_magseries, \
    time_bin_magseries, phase_bin_magseries, \
    phase_magseries_with_errs, phase_bin_magseries_with_errs

from pyeebls import eebls

from ..varbase.lcfit import spline_fit_magseries, savgol_fit_magseries, \
    traptransit_fit_magseries


############
## CONFIG ##
############

NCPUS = cpu_count()


#######################
## UTILITY FUNCTIONS ##
#######################

def auto_transit_duration(min_radius_hint,
                          max_radius_hint):
    '''
    This figures out the minimum and max transit duration (q) automatically.

    q ~ 0.076 x R**(2/3) x P**(-2/3)

    P = period in days
    R = stellar radius in solar radii

    '''




######################################
## BLS (Kovacs, Zucker, Mazeh 2002) ##
######################################

def _bls_runner(times,
                mags,
                nfreq,
                freqmin,
                stepsize,
                nbins,
                minduration,
                maxduration):
    '''
    This runs the bls.eebls function using the given inputs.

    '''

    workarr_u = np.ones(times.size)
    workarr_v = np.ones(times.size)

    blsresult = eebls(times, mags,
                      workarr_u, workarr_v,
                      nfreq, freqmin, stepsize,
                      nbins, minduration, maxduration)

    return {'power':blsresult[0],
            'bestperiod':blsresult[1],
            'bestpower':blsresult[2],
            'transdepth':blsresult[3],
            'transduration':blsresult[4],
            'transingressbin':blsresult[5],
            'transegressbin':blsresult[6]}



def parallel_bls_worker(task):
    '''
    This wraps _bls_runner for the parallel function below.

    task[0] = times
    task[1] = mags
    task[2] = nfreq
    task[3] = freqmin
    task[4] = stepsize
    task[5] = nbins
    task[6] = minduration
    task[7] = maxduration

    '''

    try:

        return _bls_runner(*task)

    except Exception as e:

        LOGEXCEPTION('BLS failed for task %s' % repr(task[2:]))

        return {
            'power':np.array([npnan for x in range(task[2])]),
            'bestperiod':npnan,
            'bestpower':npnan,
            'transdepth':npnan,
            'transduration':npnan,
            'transingressbin':npnan,
            'transegressbin':npnan
        }




def bls_serial_pfind(times, mags, errs,
                     magsarefluxes=False,
                     startp=0.1,  # search from 0.1 d to...
                     endp=100.0,  # ... 100.0 d -- don't search full timebase
                     stepsize=5.0e-4,
                     mintransitduration=0.01,  # minimum transit length in phase
                     maxtransitduration=0.8,   # maximum transit length in phase
                     nphasebins=200,
                     autofreq=True,  # figure out f0, nf, and df automatically
                     periodepsilon=0.1,
                     nbestpeaks=5,
                     sigclip=10.0,
                     verbose=True):
    '''Runs the Box Least Squares Fitting Search for transit-shaped signals.

    Based on eebls.f from Kovacs et al. 2002 and python-bls from Foreman-Mackey
    et al. 2015. This is the serial version (which is good enough in most cases
    because BLS in Fortran is fairly fast). If nfreq > 5e5, this will take a
    while.

    '''

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        # if we're setting up everything automatically
        if autofreq:

            # figure out the best number of phasebins to use
            nphasebins = int(np.ceil(2.0/mintransitduration))

            # use heuristic to figure out best timestep
            stepsize = 0.25*mintransitduration/(stimes.max()-stimes.min())

            # now figure out the frequencies to use
            minfreq = 1.0/endp
            maxfreq = 1.0/startp
            nfreq = int(np.ceil((maxfreq - minfreq)/stepsize))

            # say what we're using
            if verbose:
                LOGINFO('min P: %s, max P: %s, nfreq: %s, '
                        'minfreq: %s, maxfreq: %s' % (startp, endp, nfreq,
                                                      minfreq, maxfreq))
                LOGINFO('autofreq = True: using AUTOMATIC values for '
                        'freq stepsize: %s, nphasebins: %s, '
                        'min transit duration: %s, max transit duration: %s' %
                        (stepsize, nphasebins,
                         mintransitduration, maxtransitduration))

        else:

            minfreq = 1.0/endp
            maxfreq = 1.0/startp
            nfreq = int(np.ceil((maxfreq - minfreq)/stepsize))

            # say what we're using
            if verbose:
                LOGINFO('min P: %s, max P: %s, nfreq: %s, '
                        'minfreq: %s, maxfreq: %s' % (startp, endp, nfreq,
                                                      minfreq, maxfreq))
                LOGINFO('autofreq = False: using PROVIDED values for '
                        'freq stepsize: %s, nphasebins: %s, '
                        'min transit duration: %s, max transit duration: %s' %
                        (stepsize, nphasebins,
                         mintransitduration, maxtransitduration))


        if nfreq > 5.0e5:

            if verbose:
                LOGWARNING('more than 5.0e5 frequencies to go through; '
                           'this will take a while. '
                           'you might want to use the '
                           'periodbase.bls_parallel_pfind function instead')

        if minfreq < (1.0/(stimes.max() - stimes.min())):

            if verbose:
                LOGWARNING('the requested max P = %.3f is larger than '
                           'the time base of the observations = %.3f, '
                           ' will make minfreq = 2 x 1/timebase'
                           % (endp, stimes.max() - stimes.min()))
            minfreq = 2.0/(stimes.max() - stimes.min())
            if verbose:
                LOGINFO('new minfreq: %s, maxfreq: %s' %
                        (minfreq, maxfreq))


        # run BLS
        try:

            blsresult = _bls_runner(stimes,
                                    smags,
                                    nfreq,
                                    minfreq,
                                    stepsize,
                                    nphasebins,
                                    mintransitduration,
                                    maxtransitduration)

            # find the peaks in the BLS. this uses wavelet transforms to
            # smooth the spectrum and find peaks. a similar thing would be
            # to do a convolution with a gaussian kernel or a tophat
            # function, calculate d/dx(result), then get indices where this
            # is zero
            # blspeakinds = find_peaks_cwt(blsresults['power'],
            #                              nparray([2.0,3.0,4.0,5.0]))



            frequencies = minfreq + nparange(nfreq)*stepsize
            periods = 1.0/frequencies
            lsp = blsresult['power']

            # find the nbestpeaks for the periodogram: 1. sort the lsp array
            # by highest value first 2. go down the values until we find
            # five values that are separated by at least periodepsilon in
            # period
            # make sure to get only the finite peaks in the periodogram
            # this is needed because BLS may produce infs for some peaks
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
                        'periods':None,
                        'method':'bls',
                        'kwargs':{'startp':startp,
                                  'endp':endp,
                                  'stepsize':stepsize,
                                  'mintransitduration':mintransitduration,
                                  'maxtransitduration':maxtransitduration,
                                  'nphasebins':nphasebins,
                                  'autofreq':autofreq,
                                  'periodepsilon':periodepsilon,
                                  'nbestpeaks':nbestpeaks,
                                  'sigclip':sigclip,
                                  'magsarefluxes':magsarefluxes}}

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
                # periodepsilon to make sure we jump to an entire different
                # peak in the periodogram
                if (perioddiff > (periodepsilon*prevperiod) and
                    all(x > (periodepsilon*prevperiod)
                        for x in bestperiodsdiff)):
                    nbestperiods.append(period)
                    nbestlspvals.append(lspval)
                    peakcount = peakcount + 1

                prevperiod = period


            # generate the return dict
            resultdict = {
                'bestperiod':finperiods[bestperiodind],
                'bestlspval':finlsp[bestperiodind],
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':nbestlspvals,
                'nbestperiods':nbestperiods,
                'lspvals':lsp,
                'frequencies':frequencies,
                'periods':periods,
                'blsresult':blsresult,
                'stepsize':stepsize,
                'nfreq':nfreq,
                'nphasebins':nphasebins,
                'mintransitduration':mintransitduration,
                'maxtransitduration':maxtransitduration,
                'method':'bls',
                'kwargs':{'startp':startp,
                          'endp':endp,
                          'stepsize':stepsize,
                          'mintransitduration':mintransitduration,
                          'maxtransitduration':maxtransitduration,
                          'nphasebins':nphasebins,
                          'autofreq':autofreq,
                          'periodepsilon':periodepsilon,
                          'nbestpeaks':nbestpeaks,
                          'sigclip':sigclip,
                          'magsarefluxes':magsarefluxes}}

            return resultdict

        except Exception as e:

            LOGEXCEPTION('BLS failed!')
            return {'bestperiod':npnan,
                    'bestlspval':npnan,
                    'nbestpeaks':nbestpeaks,
                    'nbestlspvals':None,
                    'nbestperiods':None,
                    'lspvals':None,
                    'periods':None,
                    'stepsize':stepsize,
                    'nfreq':nfreq,
                    'nphasebins':nphasebins,
                    'mintransitduration':mintransitduration,
                    'maxtransitduration':maxtransitduration,
                    'method':'bls',
                    'kwargs':{'startp':startp,
                              'endp':endp,
                              'stepsize':stepsize,
                              'mintransitduration':mintransitduration,
                              'maxtransitduration':maxtransitduration,
                              'nphasebins':nphasebins,
                              'autofreq':autofreq,
                              'periodepsilon':periodepsilon,
                              'nbestpeaks':nbestpeaks,
                              'sigclip':sigclip,
                              'magsarefluxes':magsarefluxes}}


    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return {'bestperiod':npnan,
                'bestlspval':npnan,
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':None,
                'nbestperiods':None,
                'lspvals':None,
                'periods':None,
                'stepsize':stepsize,
                'nfreq':None,
                'nphasebins':None,
                'mintransitduration':mintransitduration,
                'maxtransitduration':maxtransitduration,
                'method':'bls',
                'kwargs':{'startp':startp,
                          'endp':endp,
                          'stepsize':stepsize,
                          'mintransitduration':mintransitduration,
                          'maxtransitduration':maxtransitduration,
                          'nphasebins':nphasebins,
                          'autofreq':autofreq,
                          'periodepsilon':periodepsilon,
                          'nbestpeaks':nbestpeaks,
                          'sigclip':sigclip,
                          'magsarefluxes':magsarefluxes}}



def bls_parallel_pfind(
        times, mags, errs,
        magsarefluxes=False,
        startp=0.1,  # by default, search from 0.1 d to...
        endp=100.0,  # ... 100.0 d -- don't search full timebase
        stepsize=1.0e-4,
        mintransitduration=0.01,  # minimum transit length in phase
        maxtransitduration=0.8,   # maximum transit length in phase
        nphasebins=200,
        autofreq=True,  # figure out f0, nf, and df automatically
        nbestpeaks=5,
        periodepsilon=0.1,  # 0.1
        nworkers=None,
        sigclip=10.0,
        verbose=True
):
    '''Runs the Box Least Squares Fitting Search for transit-shaped signals.

    Based on eebls.f from Kovacs et al. 2002 and python-bls from Foreman-Mackey
    et al. 2015. Breaks up the full frequency space into chunks and passes them
    to parallel BLS workers.

    NOTE: the combined BLS spectrum produced by this function is not identical
    to that produced by running BLS in one shot for the entire frequency
    space. There are differences on the order of 1.0e-3 or so in the respective
    peak values, but peaks appear at the same frequencies for both methods. This
    is likely due to different aliasing caused by smaller chunks of the
    frequency space used by the parallel workers in this function. When in
    doubt, confirm results for this parallel implementation by comparing to
    those from the serial implementation above.

    '''

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        # if we're setting up everything automatically
        if autofreq:

            # figure out the best number of phasebins to use
            nphasebins = int(np.ceil(2.0/mintransitduration))

            # use heuristic to figure out best timestep
            stepsize = 0.25*mintransitduration/(stimes.max()-stimes.min())

            # now figure out the frequencies to use
            minfreq = 1.0/endp
            maxfreq = 1.0/startp
            nfreq = int(np.ceil((maxfreq - minfreq)/stepsize))

            # say what we're using
            if verbose:
                LOGINFO('min P: %s, max P: %s, nfreq: %s, '
                        'minfreq: %s, maxfreq: %s' % (startp, endp, nfreq,
                                                      minfreq, maxfreq))
                LOGINFO('autofreq = True: using AUTOMATIC values for '
                        'freq stepsize: %s, nphasebins: %s, '
                        'min transit duration: %s, max transit duration: %s' %
                        (stepsize, nphasebins,
                         mintransitduration, maxtransitduration))

        else:

            minfreq = 1.0/endp
            maxfreq = 1.0/startp
            nfreq = int(np.ceil((maxfreq - minfreq)/stepsize))

            # say what we're using
            if verbose:
                LOGINFO('min P: %s, max P: %s, nfreq: %s, '
                        'minfreq: %s, maxfreq: %s' % (startp, endp, nfreq,
                                                      minfreq, maxfreq))
                LOGINFO('autofreq = False: using PROVIDED values for '
                        'freq stepsize: %s, nphasebins: %s, '
                        'min transit duration: %s, max transit duration: %s' %
                        (stepsize, nphasebins,
                         mintransitduration, maxtransitduration))

        # check the minimum frequency
        if minfreq < (1.0/(stimes.max() - stimes.min())):

            minfreq = 2.0/(stimes.max() - stimes.min())
            if verbose:
                LOGWARNING('the requested max P = %.3f is larger than '
                           'the time base of the observations = %.3f, '
                           ' will make minfreq = 2 x 1/timebase'
                           % (endp, stimes.max() - stimes.min()))
                LOGINFO('new minfreq: %s, maxfreq: %s' %
                        (minfreq, maxfreq))


        #############################
        ## NOW RUN BLS IN PARALLEL ##
        #############################

        # fix number of CPUs if needed
        if not nworkers or nworkers > NCPUS:
            nworkers = NCPUS
            if verbose:
                LOGINFO('using %s workers...' % nworkers)

        # break up the tasks into chunks
        frequencies = minfreq + nparange(nfreq)*stepsize

        csrem = int(fmod(nfreq, nworkers))
        csint = int(float(nfreq/nworkers))

        chunk_minfreqs, chunk_nfreqs = [], []

        for x in range(nworkers):

            this_minfreqs = frequencies[x*csint]

            # handle usual nfreqs
            if x < (nworkers - 1):
                this_nfreqs = frequencies[x*csint:x*csint+csint].size
            else:
                this_nfreqs = frequencies[x*csint:x*csint+csint+csrem].size

            chunk_minfreqs.append(this_minfreqs)
            chunk_nfreqs.append(this_nfreqs)

        # chunk_minfreqs = [frequencies[x*chunksize] for x in range(nworkers)]
        # chunk_nfreqs = [frequencies[x*chunksize:x*chunksize+chunksize].size
        #                 for x in range(nworkers)]


        # populate the tasks list
        tasks = [(stimes, smags,
                  chunk_minf, chunk_nf,
                  stepsize, nphasebins,
                  mintransitduration, maxtransitduration)
                 for (chunk_nf, chunk_minf)
                 in zip(chunk_minfreqs, chunk_nfreqs)]

        if verbose:
            for ind, task in enumerate(tasks):
                LOGINFO('worker %s: minfreq = %.6f, nfreqs = %s' %
                        (ind+1, task[3], task[2]))
            LOGINFO('running...')

        # return tasks

        # start the pool
        pool = Pool(nworkers)
        results = pool.map(parallel_bls_worker, tasks)

        pool.close()
        pool.join()
        del pool

        # now concatenate the output lsp arrays
        lsp = np.concatenate([x['power'] for x in results])
        periods = 1.0/frequencies

        # find the nbestpeaks for the periodogram: 1. sort the lsp array
        # by highest value first 2. go down the values until we find
        # five values that are separated by at least periodepsilon in
        # period

        # make sure to get only the finite peaks in the periodogram
        # this is needed because BLS may produce infs for some peaks
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
                    'periods':None,
                    'method':'bls',
                    'kwargs':{'startp':startp,
                              'endp':endp,
                              'stepsize':stepsize,
                              'mintransitduration':mintransitduration,
                              'maxtransitduration':maxtransitduration,
                              'nphasebins':nphasebins,
                              'autofreq':autofreq,
                              'periodepsilon':periodepsilon,
                              'nbestpeaks':nbestpeaks,
                              'sigclip':sigclip,
                              'magsarefluxes':magsarefluxes}}

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
            # periodepsilon to make sure we jump to an entire different
            # peak in the periodogram
            if (perioddiff > (periodepsilon*prevperiod) and
                all(x > (periodepsilon*prevperiod) for x in bestperiodsdiff)):
                nbestperiods.append(period)
                nbestlspvals.append(lspval)
                peakcount = peakcount + 1

            prevperiod = period


        # generate the return dict
        resultdict = {
            'bestperiod':finperiods[bestperiodind],
            'bestlspval':finlsp[bestperiodind],
            'nbestpeaks':nbestpeaks,
            'nbestlspvals':nbestlspvals,
            'nbestperiods':nbestperiods,
            'lspvals':lsp,
            'frequencies':frequencies,
            'periods':periods,
            'blsresult':results,
            'stepsize':stepsize,
            'nfreq':nfreq,
            'nphasebins':nphasebins,
            'mintransitduration':mintransitduration,
            'maxtransitduration':maxtransitduration,
            'method':'bls',
            'kwargs':{'startp':startp,
                      'endp':endp,
                      'stepsize':stepsize,
                      'mintransitduration':mintransitduration,
                      'maxtransitduration':maxtransitduration,
                      'nphasebins':nphasebins,
                      'autofreq':autofreq,
                      'periodepsilon':periodepsilon,
                      'nbestpeaks':nbestpeaks,
                      'sigclip':sigclip,
                      'magsarefluxes':magsarefluxes}
        }

        return resultdict

    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return {'bestperiod':npnan,
                'bestlspval':npnan,
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':None,
                'nbestperiods':None,
                'lspvals':None,
                'periods':None,
                'blsresult':None,
                'stepsize':stepsize,
                'nfreq':None,
                'nphasebins':None,
                'mintransitduration':mintransitduration,
                'maxtransitduration':maxtransitduration,
                'method':'bls',
                'kwargs':{'startp':startp,
                          'endp':endp,
                          'stepsize':stepsize,
                          'mintransitduration':mintransitduration,
                          'maxtransitduration':maxtransitduration,
                          'nphasebins':nphasebins,
                          'autofreq':autofreq,
                          'periodepsilon':periodepsilon,
                          'nbestpeaks':nbestpeaks,
                          'sigclip':sigclip,
                          'magsarefluxes':magsarefluxes}}



def bls_snr(blsdict,
            times,
            mags,
            errs,
            magsarefluxes=False,
            sigclip=10.0,
            perioddeltapercent=10,
            npeaks=None,
            assumeserialbls=False,
            verbose=True):
    '''Calculates the signal to noise ratio for each best peak in the BLS
    periodogram.

    SNR = transit model depth / RMS of light curve with transit model subtracted
          * sqrt(number of points in transit)

    blsdict is the output of either bls_parallel_pfind or bls_serial_pfind.

    times, mags, errs are ndarrays containing the magnitude series.

    perioddeltapercent controls the period interval used by a bls_serial_pfind
    run around each peak period to figure out the transit depth, duration, and
    ingress/egress bins for eventual calculation of the SNR of the peak.

    npeaks controls how many of the periods in blsdict['nbestperiods'] to find
    the SNR for. If it's None, then this will calculate the SNR for all of
    them. If it's an integer between 1 and len(blsdict['nbestperiods']), will
    calculate for only the specified number of peak periods, starting from the
    best period.

    If assumeserialbls is True, will not rerun bls_serial_pfind to figure out
    the transit depth, duration, and ingress/egress bins for eventual
    calculation of the SNR of the peak. This is normally False because we assume
    that the user will be using bls_parallel_pfind, which works on chunks of
    frequency space so returns multiple values of transit depth, duration,
    ingress/egress bin specific to those chunks. These may not be valid for the
    global best peaks in the periodogram, so we need to rerun bls_serial_pfind
    around each peak in blsdict['nbestperiods'] to get correct values for these.

    FIXME: for now, we're only doing simple RMS. Need to calculate red and
    white-noise RMS as outlined below:

      - calculate the white noise rms and the red noise rms of the residual.

        - the white noise rms is just the rms of the residual
        - the red noise rms = sqrt(binnedrms^2 - expectedbinnedrms^2)

      - calculate the SNR using:

        sqrt(delta^2 / ((sigma_w ^2 / nt) + (sigma_r ^2 / Nt))))

        where:

        delta = transit depth
        sigma_w = white noise rms
        sigma_r = red noise rms
        nt = number of in-transit points
        Nt = number of distinct transits sampled

    '''

    # figure out how many periods to work on
    if (npeaks and (0 < npeaks < len(blsdict['nbestperiods']))):
        nperiods = npeaks
    else:
        if verbose:
            LOGWARNING('npeaks not specified or invalid, '
                       'getting SNR for all %s BLS peaks' %
                       len(blsdict['nbestperiods']))
        nperiods = len(blsdict['nbestperiods'])

    nbestperiods = blsdict['nbestperiods'][:nperiods]

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        nbestsnrs = []
        nbestasnrs = []
        transitdepth, transitduration = [], []

        # get these later
        whitenoise, rednoise = [], []
        nphasebins, transingressbin, transegressbin = [], [], []

        # keep these around for diagnostics
        allsubtractedmags = []
        allphasedmags = []
        allphases = []
        allblsmodels = []

        # these are refit periods and epochs
        refitperiods = []
        refitepochs = []

        for ind, period in enumerate(nbestperiods):

            # get the period interval
            startp = period - perioddeltapercent*period/100.0
            endp = period + perioddeltapercent*period/100.0

            # see if we need to rerun bls_serial_pfind
            if not assumeserialbls:

                # run bls_serial_pfind with the kwargs copied over from the
                # initial run. replace only the startp, endp, and verbose kwarg
                # values
                prevkwargs = blsdict['kwargs'].copy()
                prevkwargs['verbose'] = verbose
                prevkwargs['startp'] = startp
                prevkwargs['endp'] = endp

                blsres = bls_serial_pfind(times, mags, errs,
                                          **prevkwargs)

            else:
                blsres = blsdict

            thistransdepth = blsres['blsresult']['transdepth']
            thistransduration = blsres['blsresult']['transduration']
            thisbestperiod = blsres['bestperiod']
            thistransingressbin = blsres['blsresult']['transingressbin']
            thistransegressbin = blsres['blsresult']['transegressbin']
            thisnphasebins = blsdict['kwargs']['nphasebins']

            try:

                # try getting the minimum light epoch using the phase bin method
                me_epochbin = int((thistransegressbin +
                                   thistransingressbin)/2.0)

                me_phases = (
                    (times - times.min())/thisbestperiod -
                    npfloor((times - times.min())/thisbestperiod)
                )
                me_phases_sortind = np.argsort(me_phases)
                me_sorted_phases = me_phases[me_phases_sortind]
                me_sorted_times = times[me_phases_sortind]

                me_bins = nplinspace(0.0, 1.0, thisnphasebins)
                me_bininds = npdigitize(me_sorted_phases, me_bins)

                me_centertransit_ind = me_bininds == me_epochbin
                me_centertransit_phase = (
                    np.median(me_sorted_phases[me_centertransit_ind])
                )
                me_centertransit_timeloc = npwhere(
                    npabs(me_sorted_phases - me_centertransit_phase) ==
                    npmin(npabs(me_sorted_phases - me_centertransit_phase))
                )
                me_centertransit_time = me_sorted_times[
                    me_centertransit_timeloc
                ]

                if me_centertransit_time.size > 1:
                    LOGWARNING('multiple possible times-of-center transits '
                               'found for period %.7f, picking the first '
                               'one from: %s' %
                               (thisbestperiod, repr(me_centertransit_time)))

                thisminepoch = me_centertransit_time[0]

            except Exception as e:

                LOGEXCEPTION(
                    'could not determine the center time of transit for '
                    'the phased LC, trying SavGol fit instead...'
                )
                # fit a Savitsky-Golay instead and get its minimum
                savfit = savgol_fit_magseries(times, mags, errs,
                                              thisbestperiod,
                                              magsarefluxes=magsarefluxes,
                                              verbose=verbose)
                thisminepoch = savfit['fitinfo']['fitepoch']


            if isinstance(thisminepoch, np.ndarray):
                if verbose:
                    LOGWARNING('minimum epoch is actually an array:\n'
                               '%s\n'
                               'instead of a float, '
                               'are there duplicate time values '
                               'in the original input? '
                               'will use the first value in this array.'
                               % repr(thisminepoch))
                thisminepoch = thisminepoch[0]

            # phase using this epoch
            phased_magseries = phase_magseries_with_errs(stimes,
                                                         smags,
                                                         serrs,
                                                         thisbestperiod,
                                                         thisminepoch,
                                                         wrap=False,
                                                         sort=True)

            tphase = phased_magseries['phase']
            tmags = phased_magseries['mags']
            terrs = phased_magseries['errs']

            # use the transit depth and duration to subtract the BLS transit
            # model from the phased mag series. we're centered about 0.0 as the
            # phase of the transit minimum so we need to look at stuff from
            # [0.0, transitphase] and [1.0-transitphase, 1.0]
            transitphase = thistransduration/2.0

            transitindices = ((tphase < transitphase) |
                              (tphase > (1.0 - transitphase)))

            # this is the BLS model
            # constant = median(tmags) outside transit
            # constant = thistransitdepth inside transit
            blsmodel = npfull_like(tmags, npmedian(tmags))

            if magsarefluxes:
                # eebls.f returns +ve depths for fluxes
                # so we need to subtract here to get fainter fluxes in transit
                blsmodel[transitindices] = (
                    blsmodel[transitindices] - thistransdepth
                )
            else:
                # eebls.f returns -ve depths for mags
                # so we need to subtract here to get fainter mags in transit
                blsmodel[transitindices] = (
                    blsmodel[transitindices] - thistransdepth
                )

            # see __init__/get_snr_of_dip docstring for description of transit
            # SNR equation, which is what we use for `thissnr`.
            subtractedmags = tmags - blsmodel
            subtractedrms = npstd(subtractedmags)
            npts_in_transit = len(tmags[transitindices])
            thissnr = (
                npsqrt(npts_in_transit) * npabs(thistransdepth/subtractedrms)
            )

            # tell user about stuff if verbose = True
            if verbose:

                LOGINFO('peak %s: new best period: %.6f, '
                        'fit center of transit: %.5f' %
                        (ind+1, thisbestperiod, thisminepoch))

                LOGINFO('transit ingress phase = %.3f to %.3f' % (1.0 -
                                                                  transitphase,
                                                                  1.0))
                LOGINFO('transit egress phase = %.3f to %.3f' % (0.0,
                                                                 transitphase))
                LOGINFO('npoints in transit: %s' % tmags[transitindices].size)

                LOGINFO('transit depth (delta): %.5f, '
                        'frac transit length (q): %.3f, '
                        ' SNR: %.3f' %
                        (thistransdepth,
                         thistransduration,
                         thissnr))

            # update the lists with results from this peak
            nbestsnrs.append(thissnr)
            transitdepth.append(thistransdepth)
            transitduration.append(thistransduration)
            transingressbin.append(thistransingressbin)
            transegressbin.append(thistransegressbin)
            nphasebins.append(thisnphasebins)

            # update the refit periods and epochs
            refitperiods.append(thisbestperiod)
            refitepochs.append(thisminepoch)

            # update the diagnostics
            allsubtractedmags.append(subtractedmags)
            allphasedmags.append(tmags)
            allphases.append(tphase)
            allblsmodels.append(blsmodel)

            # update these when we figure out how to do it
            # nphasebins.append(thisnphasebins)
            # transingressbin.append(thisingressbin)
            # transegressbin.append(thisegressbin)

        # done with working on each peak

    # if there aren't enough points in the mag series, bail out
    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        nbestsnrs, whitenoise, rednoise = None, None, None
        transitdepth, transitduration = None, None
        nphasebins, transingressbin, transegressbin = None, None, None
        allsubtractedmags, allphases, allphasedmags = None, None, None

    return {'npeaks':npeaks,
            'period':refitperiods,
            'epoch':refitepochs,
            'snr':nbestsnrs,
            'whitenoise':whitenoise,
            'rednoise':rednoise,
            'transitdepth':transitdepth,
            'transitduration':transitduration,
            'nphasebins':nphasebins,
            'transingressbin':transingressbin,
            'transegressbin':transegressbin,
            'allblsmodels':allblsmodels,
            'allsubtractedmags':allsubtractedmags,
            'allphasedmags':allphasedmags,
            'allphases':allphases}



def bls_stats_singleperiod(times, mags, errs, period,
                           magsarefluxes=False,
                           sigclip=10.0,
                           perioddeltapercent=10,
                           nphasebins=200,
                           verbose=True):
    '''This calculates the SNR, refit period, and time of center-transit for a
    single period.

    times, mags, errs are numpy arrays containing these values.

    period is the period for which the SNR, refit period, and refit epoch should
    be calculated.

    sigclip is the amount of sigmaclip to apply to the magnitude time-series.

    perioddeltapercent is used to set the search window around the specified
    period, which will be used to rerun BLS to get the transit ingress and
    egress bins.

    nphasebins is the number of phase bins to use for the BLS process. This
    should be equal to the value of nphasebins you used for your initial BLS run
    to find the specified period.

    verbose indicates whether this function should report its progress.

    This returns a dict similar to bls_snr above.

    '''

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        # get the period interval
        startp = period - perioddeltapercent*period/100.0
        endp = period + perioddeltapercent*period/100.0

        # rerun BLS in serial mode around the specified period to get the
        # transit depth, duration, ingress and egress bins
        blsres = bls_serial_pfind(times, mags, errs,
                                  verbose=verbose,
                                  startp=startp,
                                  endp=endp,
                                  nphasebins=nphasebins,
                                  magsarefluxes=magsarefluxes)

        thistransdepth = blsres['blsresult']['transdepth']
        thistransduration = blsres['blsresult']['transduration']
        thisbestperiod = blsres['bestperiod']
        thistransingressbin = blsres['blsresult']['transingressbin']
        thistransegressbin = blsres['blsresult']['transegressbin']
        thisnphasebins = nphasebins

        try:

            # try getting the minimum light epoch using the phase bin method
            me_epochbin = int((thistransegressbin +
                               thistransingressbin)/2.0)

            me_phases = (
                (times - times.min())/thisbestperiod -
                npfloor((times - times.min())/thisbestperiod)
            )
            me_phases_sortind = np.argsort(me_phases)
            me_sorted_phases = me_phases[me_phases_sortind]
            me_sorted_times = times[me_phases_sortind]

            me_bins = nplinspace(0.0, 1.0, thisnphasebins)
            me_bininds = npdigitize(me_sorted_phases, me_bins)

            me_centertransit_ind = me_bininds == me_epochbin
            me_centertransit_phase = (
                np.median(me_sorted_phases[me_centertransit_ind])
            )
            me_centertransit_timeloc = npwhere(
                npabs(me_sorted_phases - me_centertransit_phase) ==
                npmin(npabs(me_sorted_phases - me_centertransit_phase))
            )
            me_centertransit_time = me_sorted_times[
                me_centertransit_timeloc
            ]

            if me_centertransit_time.size > 1:
                LOGWARNING('multiple possible times-of-center transits '
                           'found for period %.7f, picking the first '
                           'one from: %s' %
                           (thisbestperiod, repr(me_centertransit_time)))

            thisminepoch = me_centertransit_time[0]

        except Exception as e:

            LOGEXCEPTION(
                'could not determine the center time of transit for '
                'the phased LC, trying SavGol fit instead...'
            )
            # fit a Savitsky-Golay instead and get its minimum
            savfit = savgol_fit_magseries(times, mags, errs,
                                          thisbestperiod,
                                          magsarefluxes=magsarefluxes,
                                          verbose=verbose)
            thisminepoch = savfit['fitinfo']['fitepoch']


        if isinstance(thisminepoch, np.ndarray):
            if verbose:
                LOGWARNING('minimum epoch is actually an array:\n'
                           '%s\n'
                           'instead of a float, '
                           'are there duplicate time values '
                           'in the original input? '
                           'will use the first value in this array.'
                           % repr(thisminepoch))
            thisminepoch = thisminepoch[0]

        # phase using this epoch
        phased_magseries = phase_magseries_with_errs(stimes,
                                                     smags,
                                                     serrs,
                                                     thisbestperiod,
                                                     thisminepoch,
                                                     wrap=False,
                                                     sort=True)

        tphase = phased_magseries['phase']
        tmags = phased_magseries['mags']

        # use the transit depth and duration to subtract the BLS transit
        # model from the phased mag series. we're centered about 0.0 as the
        # phase of the transit minimum so we need to look at stuff from
        # [0.0, transitphase] and [1.0-transitphase, 1.0]
        transitphase = thistransduration/2.0

        transitindices = ((tphase < transitphase) |
                          (tphase > (1.0 - transitphase)))

        # this is the BLS model
        # constant = median(tmags) outside transit
        # constant = thistransitdepth inside transit
        blsmodel = npfull_like(tmags, npmedian(tmags))

        if magsarefluxes:

            # eebls.f returns +ve transit depth for fluxes
            # so we need to subtract here to get fainter fluxes in transit
            blsmodel[transitindices] = (
                blsmodel[transitindices] - thistransdepth
            )
        else:

            # eebls.f returns -ve transit depth for magnitudes
            # so we need to subtract here to get fainter mags in transits
            blsmodel[transitindices] = (
                blsmodel[transitindices] - thistransdepth
            )

        # see __init__/get_snr_of_dip docstring for description of transit SNR
        # equation, which is what we use for `thissnr`.
        subtractedmags = tmags - blsmodel
        subtractedrms = npstd(subtractedmags)
        npts_in_transit = len(tmags[transitindices])
        thissnr = (
            npsqrt(npts_in_transit) * npabs(thistransdepth/subtractedrms)
        )

        # tell user about stuff if verbose = True
        if verbose:

            LOGINFO('refit best period: %.6f, '
                    'refit center of transit: %.5f' %
                    (thisbestperiod, thisminepoch))

            LOGINFO('transit ingress phase = %.3f to %.3f' % (1.0 -
                                                              transitphase,
                                                              1.0))
            LOGINFO('transit egress phase = %.3f to %.3f' % (0.0,
                                                             transitphase))
            LOGINFO('npoints in transit: %s' % tmags[transitindices].size)

            LOGINFO('transit depth (delta): %.5f, '
                    'frac transit length (q): %.3f, '
                    ' SNR: %.3f' %
                    (thistransdepth,
                     thistransduration,
                     thissnr))

        return {'period':thisbestperiod,
                'epoch':thisminepoch,
                'snr':thissnr,
                'whitenoise':npnan,
                'rednoise':npnan,
                'transitdepth':thistransdepth,
                'transitduration':thistransduration,
                'nphasebins':nphasebins,
                'transingressbin':thistransingressbin,
                'transegressbin':thistransegressbin,
                'blsmodel':blsmodel,
                'subtractedmags':subtractedmags,
                'phasedmags':tmags,
                'phases':tphase}


    # if there aren't enough points in the mag series, bail out
    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return None
