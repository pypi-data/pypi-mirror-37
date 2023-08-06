#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:05:57 2018

@author: Marian
"""

import itertools
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import fftconvolve


def crt_hrf_prm(varPkDelMin, varPkDelMax, varUndDelMin, varUndDelMax,
                varDelStp, varPkDspMin, varPkDspMax, varUndDspMin,
                varUndDspMax, varDspStp, varPkUndRatMin, varPkUndRatMax,
                varPkUndRatStp):

    """Create combinations of hrf parameters.

    Parameters
    ----------
    varPkDelMin : float, positive
        Minimum delay for the peak of the hrf function.
    varPkDelMax : float, positive
        Maximum delay for the peak of the hrf function.
    varUndDelMin : float, positive
        Minimum delay for the undershoot of the hrf function.
    varUndDelMax : float, positive
        Maximum delay for the undershoot of the hrf function.
    varDelStp : float, positive
        Step size for peak and undershoot delay of the hrf function.
    varPkDspMin : float, positive
        Minimum dispersion for the peak of the hrf function.
    varPkDspMax : float, positive
        Maximum dispersion for the peak of the hrf function.
    varUndDspMin : float, positive
        Minimum dispersion for the undershoot of the hrf function.
    varUndDspMax : float, positive
        Maximum dispersion for the undershoot of the hrf function.
    varDspStp : float, positive
        Step size for peak and undershoot dispersion of the hrf function.
    varPkUndRatMin : float, positive
        Minimum peak to undershoot ratio.
    varPkUndRatMax : float, positive
        Maximum peak to undershoot ratio.
    varPkUndRatStp : float, positive
        Step size for teh peak to undershoot ratio.

    Returns
    -------
    aryPrm : numpy array
        All possible hrf parameters combinations.

    """

    # Define vector for delay to peak, default: 6
    vecPkDel = np.arange(varPkDelMin, varPkDelMax+varDelStp, varDelStp)

    # Define vector for delay to undershoot, default: 16
    vecUndDel = np.arange(varUndDelMin, varUndDelMax+varDelStp, varDelStp)

    # Define vector for peak dispersion, default: 1
    vecPkDsp = np.arange(varPkDspMin, varPkDspMax+varDspStp, varDspStp)

    # Define vector for undershoot dispersion, default: 1
    vecUndDsp = np.arange(varUndDspMin, varUndDspMax+varDspStp, varDspStp)

    # Define vector for weighting of undershoot relative to peak,
    # e.g. 6 means 1:6 weighting
    vecPkUndRat = np.arange(varPkUndRatMin, varPkUndRatMax+varPkUndRatStp,
                            varPkUndRatStp)

    # Find combinations of all parameters
    # Exclude combinations where undershoot delay less than peak delay
    iterables = [vecPkDel, vecUndDel]
    vecDelCmb = list(itertools.product(*iterables))
    vecDelCmb = np.asarray(vecDelCmb)
    # Pass only the combinations where a1 < a2
    lgcDelCmb = np.less(vecDelCmb[:, 0], vecDelCmb[:, 1])
    vecDelCmb = vecDelCmb[lgcDelCmb]

    iterables = [vecDelCmb, vecPkDsp, vecUndDsp, vecPkUndRat]
    aryPrm = list(itertools.product(*iterables))
    for ind, item in enumerate(aryPrm):
        aryPrm[ind] = list(np.hstack(item))
    aryPrm = np.array(aryPrm)

    return aryPrm.astype(np.float32)


def wrp_hrf_prm_dct(vecPrm, lgcNrm=True):
    """Wrap hrf parameters into dictionary.

    Parameters
    ----------
    vecPrm : 1D numpy array
        Array with a specific combination of hrf parameters.
    lgcNrm : boolean
        Should the hrf function be passed the argument to be normalized?

    Returns
    -------
    dctPrms : dictionary
        Dictionary with hrf parameters.

    """

    # Create dictionary for hrf function
    dctPrms = {}
    dctPrms['peak_delay'] = float(vecPrm[0])
    dctPrms['under_delay'] = float(vecPrm[1])
    dctPrms['peak_disp'] = float(vecPrm[2])
    dctPrms['under_disp'] = float(vecPrm[3])
    dctPrms['p_u_ratio'] = float(vecPrm[4])

    if lgcNrm:
        dctPrms['normalize'] = True

    return dctPrms


def cvrt_hrf_prm_fn(aryPrm, fnHrf, varTr, varTmpOvsmpl, varHrfLen=32.):
    """Convert hrf parameters to hrf base function.

    Parameters
    ----------
    aryPrm : numpy array
        Array with all combinations of hrf parameters.
    fnHrf : function
        Specific hrf function that should be used
    varTr : float, positive
        Time to repeat (TR) of the (fMRI) experiment.
    varTmpOvsmpl : float, positive
        Factor by which the time courses should be temporally upsampled.
    varHrfLen : float, positive, default=32
        Length of the HRF time course in seconds.

    Returns
    -------
    aryHrfBse : 2D numpy array
        Array with hrf base functions.

    """

    # Derive array for time
    aryTme = np.linspace(0, varHrfLen, (varHrfLen // varTr) * varTmpOvsmpl)
    # Initialize array that will collect hrf base functions
    aryHrfBse = np.zeros((aryPrm.shape[0], aryTme.shape[0]), dtype=np.float32)

    # Loop over hrf parameter combinations
    for indPrm, vecPrm in enumerate(aryPrm):
        # obtain dictionary for this hrf parameter combination
        dctPrms = wrp_hrf_prm_dct(vecPrm)
        # Create hrf base function based in the parameters
        vecTmpBse = fnHrf(aryTme, **dctPrms)
        # Normalise HRF so that the sum of values is 1 (see FSL)
        # otherwise, after convolution values for predictors are very high
        vecTmpBse = np.divide(vecTmpBse, np.sum(vecTmpBse))
        # Assign normalized base function to array
        aryHrfBse[indPrm, :] = vecTmpBse

    return aryHrfBse


def cnvl_nrl_hrf(vecNrlRsp, aryHrfBse, vecFrms, vecFrmTms, varTr, varNumVol):
    """Convolution, un-vectorized, requires less RAM.

    Parameters
    ----------
    vecNrlRsp : 1D numpy array
        Neural response function taht won for this voxel in first fit.
    aryHrfBse : 2D numpy array
        All basic hrf functions.
    vecFrms : 1D numpy array
        Frame times, i.e. start point of every volume in seconds.
    vecFrmTms : 2D numpy array
        Supersampled frames times, i.e. start point of every volume in
        upsampled res.
    varTr : float, positive
        Time to repeat (TR) of the (fMRI) experiment.
    varNumVol : float, positive
        Number of volumes of the (fMRI) data.

    Returns
    -------
    aryConv : 2D numpy array
        Neural response function convolved with all possible hrf functions.

    """

    # Prepare an empty array for convolution ouput
    aryConv = np.zeros((aryHrfBse.shape[0], varNumVol),
                       dtype=np.float32)

    # Convolving the best-fitting neural response with all hrf base fn
    for indBse, vecHrfBse in enumerate(aryHrfBse):
        # Make sure hrf basis function is float64 to avoid overflow
        vecHrfBse = vecHrfBse.astype(np.float64)
        # Perform the convolution (previously: np.convolve)
        col = fftconvolve(vecHrfBse, vecNrlRsp,
                          mode='full')[:vecNrlRsp.size]
        # Get function for downsampling
        f = interp1d(vecFrmTms, col)
        # Downsample to original resoltuion to match res of data
        # take the value from the centre of each volume's period (see FSL)
        aryConv[indBse, :] = f(vecFrms + varTr/2.)

    return aryConv


def cnvl_nrl_hrf_vec(vecNrlRsp, aryHrfBse, vecFrms, vecFrmTms, varTr,
                     varNumVol):
    """Convolution, vectorized but requires more RAM.

    Parameters
    ----------
    vecNrlRsp : 1D numpy array
        Neural response function taht won for this voxel in first fit.
    aryHrfBse : 2D numpy array
        All basic hrf functions.
    vecFrms : 1D numpy array
        Frame times, i.e. start point of every volume in seconds.
    vecFrmTms : 2D numpy array
        Supersampled frames times, i.e. start point of every volume in
        upsampled res.
    varTr : float, positive
        Time to repeat (TR) of the (fMRI) experiment.
    varNumVol : float, positive
        Number of volumes of the (fMRI) data.

    Returns
    -------
    aryConv : 2D numpy array
        Neural response function convolved with all possible hrf functions.

    """

    # Perform the convolution (previously: np.convolve)
    col = fftconvolve(aryHrfBse, vecNrlRsp[None, :],
                      mode='full')[:, :vecNrlRsp.size]
    # Get function for downsampling
    f = interp1d(vecFrmTms, col)
    # Downsample to original resoltuion to match res of data
    # take the value from the centre of each volume's period (see FSL)
    aryConv = f(vecFrms + varTr/2.)

    return aryConv.astype(np.float32)


class cls_set_config(object):
    """
    Set config parameters from dictionary into local namespace.

    Parameters
    ----------
    dicCnfg : dict
        Dictionary containing parameter names (as keys) and parameter values
        (as values). For example, `dicCnfg['varTr']` contains a float, such as
        `2.94`.
    """

    def __init__(self, dicCnfg):
        """Set config parameters from dictionary into local namespace."""
        self.__dict__.update(dicCnfg)



## Create hrf parameter combinations
#aryPrm = create_hrf_params(varPkDelMin, varPkDelMax, varUndDelMin,
#                           varUndDelMax, varDelStp, varPkDspMin, varPkDspMax,
#                           varUndDspMin, varUndDspMax, varDspStp,
#                           varPkUndRatMin, varPkUndRatMax, varPkUndRatStp)
#
## Turn one parameter combination into dictionary
#dctPrms = wrap_hrf_params_dct(aryPrm, 0)
#
## Obtain hrf function with these specific hrf parameters
#t = np.arange(30)
#testBase = spm_hrf_compat(t, **dctPrms)

