#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
plotbase.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Feb 2016
License: MIT.

Contains various useful functions for plotting light curves and associated data.

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

import os
import os.path
import sys

try:
    import cPickle as pickle
except Exception as e:
    import pickle

import numpy as np
from numpy import nan as npnan, median as npmedian, \
    isfinite as npisfinite, min as npmin, max as npmax, abs as npabs, \
    ravel as npravel

# FIXME: enforce no display for now
import matplotlib
matplotlib.use('Agg')
dispok = False

import matplotlib.axes
import matplotlib.pyplot as plt

# for convolving DSS stamps to simulate seeing effects
import astropy.convolution as aconv

from astropy.io import fits as pyfits
from astropy.wcs import WCS
from astropy.visualization import MinMaxInterval, ZScaleInterval, \
    ImageNormalize, LinearStretch

try:
    import cStringIO
    from cStringIO import StringIO as strio
except Exception as e:
    from io import BytesIO as strio


###################
## LOCAL IMPORTS ##
###################

from .lcmath import phase_magseries, phase_magseries_with_errs, \
    phase_bin_magseries, phase_bin_magseries_with_errs, \
    time_bin_magseries, time_bin_magseries_with_errs, sigclip_magseries, \
    normalize_magseries, find_lc_timegroups

from .varbase.lcfit import spline_fit_magseries

from .services.skyview import get_stamp

#########################
## SIMPLE LIGHT CURVES ##
#########################

def plot_mag_series(times,
                    mags,
                    magsarefluxes=False,
                    errs=None,
                    out=None,
                    sigclip=30.0,
                    normto='globalmedian',
                    normmingap=4.0,
                    timebin=None,
                    yrange=None,
                    segmentmingap=100.0,
                    plotdpi=100):
    '''This plots a magnitude time series.

    If magsarefluxes = False, then this function reverses the y-axis as is
    customary for magnitudes. If magsarefluxes = True, then this isn't done.

    If outfile is none, then plots to matplotlib interactive window. If outfile
    is a string denoting a filename, uses that to write a png/eps/pdf figure.

    timebin is either a float indicating binsize in seconds, or None indicating
    no time-binning is required.

    sigclip is either a single float or a list of two floats. in the first case,
    the sigclip is applied symmetrically. in the second case, the first sigclip
    in the list is applied to +ve magnitude deviations (fainter) and the second
    sigclip in the list is appleid to -ve magnitude deviations (brighter).

    normto is either 'globalmedian', 'zero' or a float to normalize the mags
    to. If it's False, no normalization will be done on the magnitude time
    series. normmingap controls the minimum gap required to find possible
    groupings in the light curve that may belong to a different instrument (so
    may be displaced vertically)

    segmentmingap controls the minimum length of time (in days) required to
    consider a timegroup in the light curve as a separate segment. This is
    useful when the light curve consists of measurements taken over several
    seasons, so there's lots of dead space in the plot that can be cut out to
    zoom in on the interesting stuff. If segmentmingap is not None, the
    magseries plot will be cut in this way.

    plotdpi sets the DPI for PNG plots (default = 100).

    out is one of:

    - string name of a file to where the plot will be written
    - StringIO/BytesIO object to where the plot will be written

    '''

    # sigclip the magnitude timeseries
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)

    # now we proceed to binning
    if timebin and errs is not None:

        binned = time_bin_magseries_with_errs(stimes, smags, serrs,
                                              binsize=timebin)
        btimes, bmags, berrs = (binned['binnedtimes'],
                                binned['binnedmags'],
                                binned['binnederrs'])

    elif timebin and errs is None:

        binned = time_bin_magseries(stimes, smags,
                                    binsize=timebin)
        btimes, bmags, berrs = binned['binnedtimes'], binned['binnedmags'], None

    else:

        btimes, bmags, berrs = stimes, smags, serrs


    # check if we need to normalize
    if normto is not False:
        btimes, bmags = normalize_magseries(btimes, bmags,
                                            normto=normto,
                                            magsarefluxes=magsarefluxes,
                                            mingap=normmingap)

    btimeorigin = btimes.min()
    btimes = btimes - btimeorigin

    ##################################
    ## FINALLY PLOT THE LIGHT CURVE ##
    ##################################

    # if we're going to plot with segment gaps highlighted, then find the gaps
    if segmentmingap is not None:
        ntimegroups, timegroups = find_lc_timegroups(btimes,
                                                     mingap=segmentmingap)

    # get the yrange for all the plots if it's given
    if yrange and isinstance(yrange,(list,tuple)) and len(yrange) == 2:
        ymin, ymax = yrange

    # if it's not given, figure it out
    else:

        # the plot y limits are just 0.05 mags on each side if mags are used
        if not magsarefluxes:
            ymin, ymax = (bmags.min() - 0.05,
                          bmags.max() + 0.05)
        # if we're dealing with fluxes, limits are 2% of the flux range per side
        else:
            ycov = bmags.max() - bmags.min()
            ymin = bmags.min() - 0.02*ycov
            ymax = bmags.max() + 0.02*ycov

    # if we're supposed to make the plot segment-aware (i.e. gaps longer than
    # segmentmingap will be cut out)
    if segmentmingap and ntimegroups > 1:

        LOGINFO('%s time groups found' % ntimegroups)

        # our figure is now a multiple axis plot
        # the aspect ratio is a bit wider
        fig, axes = plt.subplots(1,ntimegroups,sharey=True)
        fig.set_size_inches(10,4.8)
        axes = np.ravel(axes)

        # now go through each axis and make the plots for each timegroup
        for timegroup, ax, axind in zip(timegroups, axes, range(len(axes))):

            tgtimes = btimes[timegroup]
            tgmags = bmags[timegroup]

            if berrs:
                tgerrs = berrs[timegroup]
            else:
                tgerrs = None

            LOGINFO('axes: %s, timegroup %s: JD %.3f to %.3f' % (
                axind,
                axind+1,
                btimeorigin + tgtimes.min(),
                btimeorigin + tgtimes.max())
            )

            ax.errorbar(tgtimes, tgmags, fmt='go', yerr=tgerrs,
                        markersize=2.0, markeredgewidth=0.0, ecolor='grey',
                        capsize=0)

            # don't use offsets on any xaxis
            ax.get_xaxis().get_major_formatter().set_useOffset(False)

            # fix the ticks to use no yoffsets and remove right spines for first
            # axes instance
            if axind == 0:
                ax.get_yaxis().get_major_formatter().set_useOffset(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.tick_left()
            # remove the right and left spines for the other axes instances
            elif 0 < axind < (len(axes)-1):
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.tick_params(right='off', labelright='off',
                               left='off',labelleft='off')
            # make the left spines invisible for the last axes instance
            elif axind == (len(axes)-1):
                ax.spines['left'].set_visible(False)
                ax.spines['right'].set_visible(True)
                ax.yaxis.tick_right()

            # set the yaxis limits
            if not magsarefluxes:
                ax.set_ylim(ymax, ymin)
            else:
                ax.set_ylim(ymin, ymax)

            # now figure out the xaxis ticklabels and ranges
            tgrange = tgtimes.max() - tgtimes.min()

            if tgrange < 10.0:
                ticklocations = [tgrange/2.0]
                ax.set_xlim(npmin(tgtimes) - 0.5, npmax(tgtimes) + 0.5)
            elif 10.0 < tgrange < 30.0:
                ticklocations = np.linspace(tgtimes.min()+5.0,
                                            tgtimes.max()-5.0,
                                            num=2)
                ax.set_xlim(npmin(tgtimes) - 2.0, npmax(tgtimes) + 2.0)

            elif 30.0 < tgrange < 100.0:
                ticklocations = np.linspace(tgtimes.min()+10.0,
                                            tgtimes.max()-10.0,
                                            num=3)
                ax.set_xlim(npmin(tgtimes) - 2.5, npmax(tgtimes) + 2.5)
            else:
                ticklocations = np.linspace(tgtimes.min()+20.0,
                                            tgtimes.max()-20.0,
                                            num=3)
                ax.set_xlim(npmin(tgtimes) - 3.0, npmax(tgtimes) + 3.0)

            ax.xaxis.set_ticks([int(x) for x in ticklocations])

        # done with plotting all the sub axes

        # make the distance between sub plots smaller
        plt.subplots_adjust(wspace=0.07)

        # make the overall x and y labels
        fig.text(0.5, 0.00, 'JD - %.3f (not showing gaps > %.2f d)' %
                 (btimeorigin, segmentmingap), ha='center')
        if not magsarefluxes:
            fig.text(0.02, 0.5, 'magnitude', va='center', rotation='vertical')
        else:
            fig.text(0.02, 0.5, 'flux', va='center', rotation='vertical')


    # make normal figure otherwise
    else:

        fig = plt.figure()
        fig.set_size_inches(7.5,4.8)

        plt.errorbar(btimes, bmags, fmt='go', yerr=berrs,
                     markersize=2.0, markeredgewidth=0.0, ecolor='grey',
                     capsize=0)

        # make a grid
        plt.grid(color='#a9a9a9',
                 alpha=0.9,
                 zorder=0,
                 linewidth=1.0,
                 linestyle=':')

        # fix the ticks to use no offsets
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

        plt.xlabel('JD - %.3f' % btimeorigin)

        # set the yaxis limits and labels
        if not magsarefluxes:
            plt.ylim(ymax, ymin)
            plt.ylabel('magnitude')
        else:
            plt.ylim(ymin, ymax)
            plt.ylabel('flux')

    # check if the output filename is actually an instance of StringIO
    if sys.version_info[:2] < (3,0):

        is_strio = isinstance(out, cStringIO.InputType)

    else:

        is_strio = isinstance(out, strio)


    # write the plot out to a file if requested
    if out and not is_strio:

        if out.endswith('.png'):
            plt.savefig(out,bbox_inches='tight',dpi=plotdpi)
        else:
            plt.savefig(out,bbox_inches='tight')
        plt.close()
        return os.path.abspath(out)

    elif out and is_strio:

        plt.savefig(out, bbox_inches='tight', dpi=plotdpi, format='png')
        return out

    elif not out and dispok:

        plt.show()
        plt.close()
        return

    else:

        LOGWARNING('no output file specified and no $DISPLAY set, '
                   'saving to magseries-plot.png in current directory')
        outfile = 'magseries-plot.png'
        plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
        plt.close()
        return os.path.abspath(outfile)


def plot_magseries(times,
                   mags,
                   magsarefluxes=False,
                   errs=None,
                   out=None,
                   sigclip=30.0,
                   normto='globalmedian',
                   normmingap=4.0,
                   timebin=None,
                   yrange=None,
                   segmentmingap=100.0,
                   plotdpi=100):
    '''This wraps plot_mag_series.

    '''

    return plot_mag_series(times,
                           mags,
                           magsarefluxes=magsarefluxes,
                           errs=errs,
                           out=out,
                           sigclip=sigclip,
                           normto=normto,
                           normmingap=normmingap,
                           timebin=timebin,
                           yrange=yrange,
                           segmentmingap=100.0,
                           plotdpi=plotdpi)



#########################
## PHASED LIGHT CURVES ##
#########################

def plot_phased_mag_series(times,
                           mags,
                           period,
                           magsarefluxes=False,
                           errs=None,
                           normto='globalmedian',
                           normmingap=4.0,
                           epoch='min',
                           outfile=None,
                           sigclip=30.0,
                           phasewrap=True,
                           phasesort=True,
                           phasebin=None,
                           plotphaselim=(-0.8,0.8),
                           fitknotfrac=0.01,
                           yrange=None,
                           plotdpi=100,
                           modelmags=None,
                           modeltimes=None,
                           modelerrs=None):
    '''This plots a phased magnitude time series using the period provided.

    Args
    ----

    times, mags:
            ndarrays of time and magnitude time series values (flux
            values if magsarefluxes = True)

    period:
        the period to use to phase fold the time series.

    errs (np.ndarray):
        if None, does not show error bars (otherwise, it does).

    epoch (float/None/str):
        - if None, uses the min(times) as the epoch.
        - if epoch is the string 'min', then fits a cubic spline to the
          phased light curve using min(times), finds the magnitude minimum
          from the fitted light curve, then uses the corresponding time value
          as the epoch.
        - if epoch is a float, then uses that directly to phase the light
          curve and as the epoch of the phased mag series plot.

    modelmags, modeltimes, modelerrs (np.ndarray/None):
        - if None, nothing happens.
        - if np.ndarray, also overplots a model transit to the phased
          lightcurve (e.g., fit using lcfit.mandelagol_fit_magseries).

    outfile (float/None/str):
        - a string filename for the file where the plot will be written
        - a StringIO/BytesIO object to where the plot will be written
        - a matplotlib.axes.Axes object to where the plot will be written
        - if None, plots to magseries-phased-plot.png in current dir

    plotdpi (int): sets the DPI for PNG plots.


    Returns
    -------

    as specified in the outfile kwarg.

    '''

    # sigclip the magnitude timeseries
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # check if we need to normalize
    if normto is not False:
        stimes, smags = normalize_magseries(stimes, smags,
                                            normto=normto,
                                            magsarefluxes=magsarefluxes,
                                            mingap=normmingap)

        if ( isinstance(modelmags, np.ndarray) and
             isinstance(modeltimes, np.ndarray) ):

            stimes, smags = normalize_magseries(modeltimes, modelmags,
                                                normto=normto,
                                                magsarefluxes=magsarefluxes,
                                                mingap=normmingap)

    # figure out the epoch, if it's None, use the min of the time
    if epoch is None:
        epoch = stimes.min()

    # if the epoch is 'min', then fit a spline to the light curve phased
    # using the min of the time, find the fit mag minimum and use the time for
    # that as the epoch
    elif isinstance(epoch, str) and epoch == 'min':

        try:
            spfit = spline_fit_magseries(stimes, smags, serrs, period,
                                         knotfraction=fitknotfrac)
            epoch = spfit['fitinfo']['fitepoch']
            if len(epoch) != 1:
                epoch = epoch[0]
        except Exception as e:
            LOGEXCEPTION('spline fit failed, using min(times) as epoch')
            epoch = npmin(stimes)


    # now phase the data light curve (and optionally, phase bin the light curve)
    if errs is not None:

        phasedlc = phase_magseries_with_errs(stimes, smags, serrs, period,
                                             epoch, wrap=phasewrap,
                                             sort=phasesort)
        plotphase = phasedlc['phase']
        plotmags = phasedlc['mags']
        ploterrs = phasedlc['errs']

        # if we're supposed to bin the phases, do so
        if phasebin:

            binphasedlc = phase_bin_magseries_with_errs(plotphase, plotmags,
                                                        ploterrs,
                                                        binsize=phasebin)
            binplotphase = binphasedlc['binnedphases']
            binplotmags = binphasedlc['binnedmags']
            binploterrs = binphasedlc['binnederrs']

    else:

        phasedlc = phase_magseries(stimes, smags, period, epoch,
                                   wrap=phasewrap, sort=phasesort)
        plotphase = phasedlc['phase']
        plotmags = phasedlc['mags']
        ploterrs = None

        # if we're supposed to bin the phases, do so
        if phasebin:

            binphasedlc = phase_bin_magseries(plotphase,
                                              plotmags,
                                              binsize=phasebin)
            binplotphase = binphasedlc['binnedphases']
            binplotmags = binphasedlc['binnedmags']
            binploterrs = None

    # phase the model light curve
    modelplotphase, modelplotmags, modelploterrs = None, None, None

    if ( isinstance(modelerrs,np.ndarray) and
         isinstance(modeltimes,np.ndarray) and
         isinstance(modelmags,np.ndarray) ):

        modelphasedlc = phase_magseries_with_errs(modeltimes, modelmags,
                                                  modelerrs, period, epoch,
                                                  wrap=phasewrap,
                                                  sort=phasesort)
        modelplotphase = modelphasedlc['phase']
        modelplotmags = modelphasedlc['mags']
        modelploterrs = modelphasedlc['errs']

    # note that we never will phase-bin the model (no point).
    elif ( not isinstance(modelerrs,np.ndarray) and
           isinstance(modeltimes,np.ndarray) and
           isinstance(modelmags,np.ndarray) ):

        modelphasedlc = phase_magseries(modeltimes, modelmags, period, epoch,
                                        wrap=phasewrap, sort=phasesort)
        modelplotphase = modelphasedlc['phase']
        modelplotmags = modelphasedlc['mags']

    # finally, make the plots

    # check if the outfile is actually an Axes object
    if isinstance(outfile, matplotlib.axes.Axes):
        ax = outfile

    # otherwise, it's just a normal file or StringIO/BytesIO
    else:
        fig = plt.figure()
        fig.set_size_inches(7.5,4.8)
        ax = plt.gca()

    if phasebin:
        ax.errorbar(plotphase, plotmags, fmt='o',
                    color='#B2BEB5',
                    yerr=ploterrs,
                    markersize=3.0,
                    markeredgewidth=0.0,
                    ecolor='#B2BEB5',
                    capsize=0)
        ax.errorbar(binplotphase, binplotmags, fmt='bo', yerr=binploterrs,
                    markersize=5.0, markeredgewidth=0.0, ecolor='#B2BEB5',
                    capsize=0)

    else:
        ax.errorbar(plotphase, plotmags, fmt='ko', yerr=ploterrs,
                    markersize=3.0, markeredgewidth=0.0, ecolor='#B2BEB5',
                    capsize=0)

    if (isinstance(modelplotphase, np.ndarray) and
        isinstance(modelplotmags, np.ndarray)):

        ax.plot(modelplotphase, modelplotmags, zorder=5, linewidth=2,
                alpha=0.9, color='#181c19')

    # make a grid
    ax.grid(color='#a9a9a9',
            alpha=0.9,
            zorder=0,
            linewidth=1.0,
            linestyle=':')

    # make lines for phase 0.0, 0.5, and -0.5
    ax.axvline(0.0,alpha=0.9,linestyle='dashed',color='g')
    ax.axvline(-0.5,alpha=0.9,linestyle='dashed',color='g')
    ax.axvline(0.5,alpha=0.9,linestyle='dashed',color='g')

    # fix the ticks to use no offsets
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)

    # get the yrange
    if yrange and isinstance(yrange,(list,tuple)) and len(yrange) == 2:
        ymin, ymax = yrange
    else:
        ymin, ymax = ax.get_ylim()

    # set the y axis labels and range
    if not magsarefluxes:
        ax.set_ylim(ymax, ymin)
        yaxlabel = 'magnitude'
    else:
        ax.set_ylim(ymin, ymax)
        yaxlabel = 'flux'

    # set the x axis limit
    if not plotphaselim:
        ax.set_xlim((npmin(plotphase)-0.1,
                     npmax(plotphase)+0.1))
    else:
        ax.set_xlim((plotphaselim[0],plotphaselim[1]))

    # set up the axis labels and plot title
    ax.set_xlabel('phase')
    ax.set_ylabel(yaxlabel)
    ax.set_title('period: %.6f d - epoch: %.6f' % (period, epoch))

    LOGINFO('using period: %.6f d and epoch: %.6f' % (period, epoch))

    # check if the output filename is actually an instance of StringIO
    if sys.version_info[:2] < (3,0):

        is_strio = isinstance(outfile, cStringIO.InputType)

    else:

        is_strio = isinstance(outfile, strio)

    # make the figure
    if (outfile and
        not is_strio and
        not isinstance(outfile, matplotlib.axes.Axes)):

        if outfile.endswith('.png'):
            fig.savefig(outfile, bbox_inches='tight', dpi=plotdpi)
        else:
            fig.savefig(outfile, bbox_inches='tight')
        plt.close()
        return period, epoch, os.path.abspath(outfile)

    elif outfile and is_strio:

        fig.savefig(outfile, bbox_inches='tight', dpi=plotdpi, format='png')
        return outfile

    elif outfile and isinstance(outfile, matplotlib.axes.Axes):

        return outfile

    elif not outfile and dispok:

        plt.show()
        plt.close()
        return period, epoch

    else:

        LOGWARNING('no output file specified and no $DISPLAY set, '
                   'saving to magseries-phased-plot.png in current directory')
        outfile = 'magseries-phased-plot.png'
        plt.savefig(outfile, bbox_inches='tight', dpi=plotdpi)
        plt.close()
        return period, epoch, os.path.abspath(outfile)



def plot_phased_magseries(times,
                          mags,
                          period,
                          magsarefluxes=False,
                          errs=None,
                          normto='globalmedian',
                          normmingap=4.0,
                          epoch='min',
                          outfile=None,
                          sigclip=30.0,
                          phasewrap=True,
                          phasesort=True,
                          phasebin=None,
                          plotphaselim=(-0.8,0.8),
                          fitknotfrac=0.01,
                          yrange=None,
                          plotdpi=100,
                          modelmags=None,
                          modeltimes=None,
                          modelerrs=None):
    '''This wraps plot_phased_mag_series for consistent API with lcfit functions.

    '''

    return plot_phased_mag_series(
        times,
        mags,
        period,
        magsarefluxes=magsarefluxes,
        errs=errs,
        normto=normto,
        normmingap=normmingap,
        epoch=epoch,
        outfile=outfile,
        sigclip=sigclip,
        phasewrap=phasewrap,
        phasesort=phasesort,
        phasebin=phasebin,
        plotphaselim=plotphaselim,
        fitknotfrac=fitknotfrac,
        yrange=yrange,
        plotdpi=plotdpi,
        modelmags=modelmags,
        modeltimes=modeltimes,
        modelerrs=modelerrs
    )



##########################
## PLOTTING FITS IMAGES ##
##########################

def skyview_stamp(ra, decl,
                  survey='DSS2 Red',
                  scaling='Linear',
                  flip=True,
                  convolvewith=None,
                  forcefetch=False,
                  cachedir='~/.astrobase/stamp-cache',
                  timeout=10.0,
                  retry_failed=False,
                  savewcsheader=True,
                  verbose=False):
    '''This is the internal version of the astroquery_skyview_stamp function.

    Why this exists:

    - SkyView queries don't accept timeouts (should put in a PR for this)
    - we can drop the dependency on astroquery (but add another on requests)

    flip = True will flip the image top to bottom.

    if convolvewith is an astropy.convolution kernel:

    http://docs.astropy.org/en/stable/convolution/kernels.html

    this will return the stamp convolved with that kernel. This can be useful to
    see effects of wide-field telescopes (like the HATNet and HATSouth lenses)
    degrading the nominal 1 arcsec/px of DSS, causing blending of targets and
    any variability.

    cachedir points to the astrobase stamp-cache directory.

    '''

    stampdict = get_stamp(ra, decl,
                          survey=survey,
                          scaling=scaling,
                          forcefetch=forcefetch,
                          cachedir=cachedir,
                          timeout=timeout,
                          retry_failed=retry_failed,
                          verbose=verbose)
    #
    # DONE WITH FETCHING STUFF
    #
    if stampdict:

        # open the frame
        stampfits = pyfits.open(stampdict['fitsfile'])
        header = stampfits[0].header
        frame = stampfits[0].data
        stampfits.close()

        # finally, we can process the frame
        if flip:
            frame = np.flipud(frame)

        if verbose:
            LOGINFO('fetched stamp successfully for (%.3f, %.3f)'
                    % (ra, decl))


        if convolvewith:

            convolved = aconv.convolve(frame, convolvewith)
            if savewcsheader:
                return convolved, header
            else:
                return convolved

        else:

            if savewcsheader:
                return frame, header
            else:
                return frame

    else:
        LOGERROR('could not fetch the requested stamp for '
                 'coords: (%.3f, %.3f) from survey: %s and scaling: %s'
                 % (ra, decl, survey, scaling))
        return None



def fits_finder_chart(
        fitsfile,
        outfile,
        wcsfrom=None,
        scale=ZScaleInterval(),
        stretch=LinearStretch(),
        colormap=plt.cm.gray_r,
        findersize=None,
        finder_coordlimits=None,
        overlay_ra=None,
        overlay_decl=None,
        overlay_pltopts={'marker':'o',
                         'markersize':10.0,
                         'markerfacecolor':'none',
                         'markeredgewidth':2.0,
                         'markeredgecolor':'red'},
        overlay_zoomcontain=False,
        grid=False,
        gridcolor='k'
):
    '''This makes a finder chart from fitsfile with an optional object position
    overlay.

    Args
    ----

    `fitsfile` is the FITS file to use to make the finder chart

    `outfile` is the name of the output file. This can be a png or pdf or
    whatever else matplotlib can write given a filename and extension.

    If `wcsfrom` is None, the WCS to transform the RA/Dec to pixel x/y will be
    taken from the FITS header of `fitsfile`. If this is not None, it must be a
    FITS or similar file that contains a WCS header in its first extension.

    `scale` sets the normalization for the FITS pixel values. This is an
    astropy.visualization Interval object.

    `stretch` sets the stretch function for mapping FITS pixel values to output
    pixel values. This is an astropy.visualization Stretch object.

    See http://docs.astropy.org/en/stable/visualization/normalization.html for
    details on `scale` and `stretch` objects.

    `colormap` is a matplotlib color map object to use for the output image.

    If `findersize` is None, the output image size will be set by the NAXIS1 and
    NAXIS2 keywords in the input `fitsfile` FITS header. Otherwise, `findersize`
    must be a tuple with the intended x and y size of the image in inches (all
    output images will use a DPI = 100).

    `finder_coordlimits` sets x and y limits for the plot, effectively zooming
    it in if these are smaller than the dimensions of the FITS image. This
    should be a list of the form: [minra, maxra, mindecl, maxdecl] all in
    decimal degrees.

    `overlay_ra` and `overlay_decl` are ndarrays containing the RA and Dec
    values to overplot on the image as an overlay.

    `overlay_pltopts` controls how the overlay points will be plotted. This a
    dict with standard matplotlib marker, etc. kwargs.

    `overlay_zoomcontain` controls if the finder chart will be zoomed to just
    contain the overlayed points. Everything outside the footprint of these
    points will be discarded.

    `grid` sets if a grid will be made on the output image.

    `gridcolor` sets the color of the grid lines. This is a usual matplotib
    color spec string.


    Returns
    -------

    The filename of the generated output image if successful. None otherwise.

    '''

    # read in the FITS file
    if wcsfrom is None:

        hdulist = pyfits.open(fitsfile)
        img, hdr = hdulist[0].data, hdulist[0].header
        hdulist.close()

        frameshape = (hdr['NAXIS1'], hdr['NAXIS2'])
        w = WCS(hdr)

    elif os.path.exists(wcsfrom):

        hdulist = pyfits.open(fitsfile)
        img, hdr = hdulist[0].data, hdulist[0].header
        hdulist.close()

        frameshape = (hdr['NAXIS1'], hdr['NAXIS2'])
        w = WCS(wcsfrom)

    else:

        LOGERROR('could not determine WCS info for input FITS: %s' %
                 fitsfile)
        return None

    # use the frame shape to set the output PNG's dimensions
    if findersize is None:
        fig = plt.figure(figsize=(frameshape[0]/100.0,
                                  frameshape[1]/100.0))
    else:
        fig = plt.figure(figsize=findersize)


    # set the coord limits if zoomcontain is True
    # we'll leave 30 arcseconds of padding on each side
    if (overlay_zoomcontain and
        overlay_ra is not None and
        overlay_decl is not None):

        finder_coordlimits = [overlay_ra.min()-30.0/3600.0,
                              overlay_ra.max()+30.0/3600.0,
                              overlay_decl.min()-30.0/3600.0,
                              overlay_decl.max()+30.0/3600.0]


    # set the coordinate limits if provided
    if finder_coordlimits and isinstance(finder_coordlimits, (list,tuple)):

        minra, maxra, mindecl, maxdecl = finder_coordlimits
        cntra, cntdecl = (minra + maxra)/2.0, (mindecl + maxdecl)/2.0

        pixelcoords = w.all_world2pix([[minra, mindecl],
                                       [maxra, maxdecl],
                                       [cntra, cntdecl]],1)
        x1, y1, x2, y2 = (int(pixelcoords[0,0]),
                          int(pixelcoords[0,1]),
                          int(pixelcoords[1,0]),
                          int(pixelcoords[1,1]))

        xmin = x1 if x1 < x2 else x2
        xmax = x2 if x2 > x1 else x1

        ymin = y1 if y1 < y2 else y2
        ymax = y2 if y2 > y1 else y1

        # create a new WCS with the same transform but new center coordinates
        whdr = w.to_header()
        whdr['CRPIX1'] = (xmax - xmin)/2
        whdr['CRPIX2'] = (ymax - ymin)/2
        whdr['CRVAL1'] = cntra
        whdr['CRVAL2'] = cntdecl
        whdr['NAXIS1'] = xmax - xmin
        whdr['NAXIS2'] = ymax - ymin
        w = WCS(whdr)

    else:
        xmin, xmax, ymin, ymax = 0, hdr['NAXIS2'], 0, hdr['NAXIS1']

    # add the axes with the WCS projection
    # this should automatically handle subimages because we fix the WCS
    # appropriately above for these
    fig.add_subplot(111,projection=w)

    if scale is not None and stretch is not None:

        norm = ImageNormalize(img,
                              interval=scale,
                              stretch=stretch)

        plt.imshow(img[ymin:ymax,xmin:xmax],
                   origin='lower',
                   cmap=colormap,
                   norm=norm)

    else:

        plt.imshow(img[ymin:ymax,xmin:xmax],
                   origin='lower',
                   cmap=colormap)


    # handle additional options
    if grid:
        plt.grid(color=gridcolor,ls='solid',lw=1.0)

    # handle the object overlay
    if overlay_ra is not None and overlay_decl is not None:

        our_pltopts = dict(
            transform=plt.gca().get_transform('fk5'),
            marker='o',
            markersize=10.0,
            markerfacecolor='none',
            markeredgewidth=2.0,
            markeredgecolor='red',
            rasterized=True,
            linestyle='none'
        )
        if overlay_pltopts is not None and isinstance(overlay_pltopts,
                                                      dict):
            our_pltopts.update(overlay_pltopts)


        plt.gca().set_autoscale_on(False)
        plt.gca().plot(overlay_ra, overlay_decl,
                       **our_pltopts)

    plt.xlabel('Right Ascension [deg]')
    plt.ylabel('Declination [deg]')

    # get the x and y axes objects to fix the ticks
    xax = plt.gca().coords[0]
    yax = plt.gca().coords[1]

    yax.set_major_formatter('d.ddd')
    xax.set_major_formatter('d.ddd')

    # save the figure
    plt.savefig(outfile, dpi=100.0)
    plt.close('all')

    return outfile



##################
## PERIODOGRAMS ##
##################

PLOTYLABELS = {'gls':'Generalized Lomb-Scargle normalized power',
               'pdm':r'Stellingwerf PDM $\Theta$',
               'aov':r'Schwarzenberg-Czerny AoV $\Theta$',
               'mav':r'Schwarzenberg-Czerny AoVMH $\Theta$',
               'bls':'Box Least-squared Search SR',
               'acf':'Autocorrelation Function',
               'sls':'Lomb-Scargle normalized power',
               'win':'Lomb-Scargle normalized power'}

METHODLABELS = {'gls':'Generalized Lomb-Scargle periodogram',
                'pdm':'Stellingwerf phase-dispersion minimization',
                'aov':'Schwarzenberg-Czerny AoV',
                'mav':'Schwarzenberg-Czerny AoV multi-harmonic',
                'bls':'Box Least-squared Search',
                'acf':'McQuillan+ ACF Period Search',
                'sls':'Lomb-Scargle periodogram (Scipy)',
                'win':'Timeseries Sampling Lomb-Scargle periodogram'}

METHODSHORTLABELS = {'gls':'Generalized L-S',
                     'pdm':'Stellingwerf PDM',
                     'aov':'Schwarzenberg-Czerny AoV',
                     'mav':'Schwarzenberg-Czerny AoVMH',
                     'acf':'McQuillan+ ACF',
                     'bls':'BLS',
                     'sls':'L-S (Scipy)',
                     'win':'Sampling L-S'}


def plot_periodbase_lsp(lspinfo, outfile=None, plotdpi=100):

    '''Makes a plot of periodograms obtained from periodbase functions.

    If lspinfo is a dictionary, uses the information directly. If it's a
    filename string ending with .pkl, then this assumes it's a periodbase LSP
    pickle and loads the corresponding info from it.

    '''

    # get the lspinfo from a pickle file transparently
    if isinstance(lspinfo,str) and os.path.exists(lspinfo):
        LOGINFO('loading LSP info from pickle %s' % lspinfo)
        with open(lspinfo,'rb') as infd:
            lspinfo = pickle.load(infd)

    try:

        # get the things to plot out of the data
        periods = lspinfo['periods']
        lspvals = lspinfo['lspvals']
        bestperiod = lspinfo['bestperiod']
        lspmethod = lspinfo['method']

        # make the LSP plot on the first subplot
        plt.plot(periods, lspvals)
        plt.xscale('log',basex=10)
        plt.xlabel('Period [days]')
        plt.ylabel(PLOTYLABELS[lspmethod])
        plottitle = '%s best period: %.6f d' % (METHODSHORTLABELS[lspmethod],
                                                bestperiod)
        plt.title(plottitle)

        # show the best five peaks on the plot
        for bestperiod, bestpeak in zip(lspinfo['nbestperiods'],
                                        lspinfo['nbestlspvals']):

            plt.annotate('%.6f' % bestperiod,
                         xy=(bestperiod, bestpeak), xycoords='data',
                         xytext=(0.0,25.0), textcoords='offset points',
                         arrowprops=dict(arrowstyle="->"),fontsize='x-small')

        # make a grid
        plt.grid(color='#a9a9a9',
                 alpha=0.9,
                 zorder=0,
                 linewidth=1.0,
                 linestyle=':')

        # make the figure
        if outfile and isinstance(outfile, str):

            if outfile.endswith('.png'):
                plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
            else:
                plt.savefig(outfile,bbox_inches='tight')

            plt.close()
            return os.path.abspath(outfile)

        elif dispok:

            plt.show()
            plt.close()
            return

        else:

            LOGWARNING('no output file specified and no $DISPLAY set, '
                       'saving to lsp-plot.png in current directory')
            outfile = 'lsp-plot.png'
            plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
            plt.close()
            return os.path.abspath(outfile)

    except Exception as e:

        LOGEXCEPTION('could not plot this LSP, appears to be empty')
        return
