# -*- coding: utf-8 -*-
"""Find best fitting hrf parameters."""

# Part of hrf_opt library
# Copyright (C) 2018  Marian Schneider
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from sklearn.model_selection import KFold
from pyprf_feature.analysis.utils_hrf import spm_hrf_compat

from hrf_opt.find_hrf_utils_cy_one import (cy_lst_sq_one, cy_lst_sq_xval_one)
#from hrf_opt.find_hrf_utils_cy_two import (cy_lst_sq_two, cy_lst_sq_xval_two)
from hrf_opt.hrf_opt_utils import (cnvl_nrl_hrf, cnvl_nrl_hrf_vec,
                                   cvrt_hrf_prm_fn)


def find_opt_hrf(idxPrc, aryFunc, aryNrlRsp, aryHrfBse, aryPrm, varTr,
                 varNumVol, varTmpOvsmpl, lgcXval, varNumXval, queOut,
                 lgcPrint=True):
    """
    Find best hrf parameters for voxel time course, using the CPU.

    Parameters
    ----------
    idxPrc : int
        Process ID of the process calling this function (for CPU
        multi-threading). In GPU version, this parameter is 0 (just one thread
        on CPU).
    aryFunc : np.array
        2D array with functional MRI data, with shape aryFunc[voxel, time].
    aryNrlRsp : np.array
        Array with best fitting neural response.
    aryHrfBse : np.array
        2D array with all basis hrf functions.
    aryPrm : np.array
        2D array with all hrf parameter combinations.
    varTr : float, positive
        Time to repeat (TR) of the (fMRI) experiment.
    varNumVol : float, positive
        Number of volumes of the (fMRI) data.
    varTmpOvsmpl : float, positive
        Factor by which the time courses has been temporally upsampled.
    lgcXval: boolean
        Logical to determine whether we cross-validate.
    varNumXval: int
        Number of folds for k-fold cross-validation.
    queOut : multiprocessing.queues.Queue
        Queue to put the results on.
    lgcPrint : boolean
        Whether print statements should be executed.

    Returns
    -------
    lstOut : list
        List containing the following objects:
        idxPrc : int
            Process ID of the process calling this function (for CPU
            multi-threading). In GPU version, this parameter is 0.
        vecBstXpos : np.array
            1D array with best fitting x-position for each voxel, with shape
            vecBstXpos[voxel].
        vecBstYpos : np.array
            1D array with best fitting y-position for each voxel, with shape
            vecBstYpos[voxel].
        vecBstSd : np.array
            1D array with best fitting pRF size for each voxel, with shape
            vecBstSd[voxel].
        vecBstR2 : np.array
            1D array with R2 value of 'winning' pRF model for each voxel, with
            shape vecBstR2[voxel].
        aryBstBts : np.array
            2D array with beta parameter estimates of 'winning' pRF model for
            each voxel, with shape aryBstBts[voxel, feautures].

    Notes
    -----
    The list with results is not returned directly, but placed on a
    multiprocessing queue. This version performs the model finding on the CPU,
    using cython.

    """

    # Until implemented otherwise, set number of features to 1 here
    varNumFtr = 1

    # Number of voxels to be fitted in this chunk:
    varNumVoxChnk = aryFunc.shape[-1]

    # Number of models:
    varNumMdls = aryHrfBse.shape[0]

    # Make array to collect residuals for all voxels and models
    aryClcRes = np.zeros((varNumVoxChnk, varNumMdls)).astype(np.float32)

    # Vectors for hrf finding results.
    # Make sure they have the same precision as aryPrm, since this
    # is important for later comparison
    vecBstPrm = np.zeros((varNumVoxChnk, aryPrm.shape[-1]), dtype=aryPrm.dtype)

    # Vector for best R-square value. For each model fit, the R-square value is
    # compared to this, and updated if it is lower than the best-fitting
    # solution so far. We initialise with an arbitrary, high value
    vecBstRes = np.add(np.zeros(varNumVoxChnk), np.inf).astype(np.float32)

    # array for best beta values. If we update the residual value above because
    # it is lower, we also update the beta values of these voxels
    aryBstBts = np.zeros((varNumVoxChnk, 1)).astype(np.float32)

    # In case we cross-validate we also save and replace the best
    # residual values for every fold (not only mean across folds):
    if lgcXval:
        aryBstResFlds = np.zeros((varNumVoxChnk, varNumXval), dtype=np.float32)

    # Set type to float 32:
    aryFunc = aryFunc.astype(np.float32)

    # if lgc for Xval is true we already prepare indices for xvalidation
    if lgcXval:
        # obtain iterator for cross-validation
        itXval = KFold(n_splits=varNumXval)
        vecSplts = np.arange(aryFunc.shape[0], dtype=np.int32)

        # prepare lists that will hold indices for xvalidation
        lstIdxTrn = []
        lstIdxtst = []
        # Loop over the cross-validations to put indcies in array
        for idxTrn, idxTst in itXval.split(vecSplts):
            lstIdxTrn.append(idxTrn)
            lstIdxtst.append(idxTst)
        # trun lists into array
        aryIdxTrn = np.stack(lstIdxTrn, axis=-1).astype(np.int32)
        aryIdxTst = np.stack(lstIdxtst, axis=-1).astype(np.int32)

    # Prepare status indicator if this is the first of the parallel processes:
    if idxPrc == 0:

        # We create a status indicator for the time consuming pRF model finding
        # algorithm. Number of steps of the status indicator:
        varStsStpSze = 20

        # Vector with pRF values at which to give status feedback:
        vecStatPrf = np.linspace(0,
                                 varNumVoxChnk,
                                 num=(varStsStpSze+1),
                                 endpoint=True)
        vecStatPrf = np.ceil(vecStatPrf)
        vecStatPrf = vecStatPrf.astype(int)

        # Vector with corresponding percentage values at which to give status
        # feedback:
        vecStatPrc = np.linspace(0,
                                 100,
                                 num=(varStsStpSze+1),
                                 endpoint=True)
        vecStatPrc = np.ceil(vecStatPrc)
        vecStatPrc = vecStatPrc.astype(int)

        # Counter for status indicator:
        varCntSts01 = 0
        varCntSts02 = 0

    # Loop through voxels:
    for idxVxl in range(0, varNumVoxChnk):

        # Status indicator (only used in the first of the parallel
        # processes):
        if idxPrc == 0:

            # Status indicator:
            if varCntSts02 == vecStatPrf[varCntSts01]:

                # Prepare status message:
                strStsMsg = ('------------Progress: ' +
                             str(vecStatPrc[varCntSts01]) +
                             ' % --- ' +
                             str(vecStatPrf[varCntSts01]) +
                             ' voxels out of ' +
                             str(varNumVoxChnk))
                if lgcPrint:
                    print(strStsMsg)

                # Only increment counter if the last value has not been
                # reached yet:
                if varCntSts01 < varStsStpSze:
                    varCntSts01 = varCntSts01 + int(1)

        # For this particular voxel get best-fitting neural response
        vecNrlRsp = aryNrlRsp[idxVxl, :].astype(np.float32)
        # Get frame times, i.e. start point of every volume in seconds
        vecFrms = np.arange(0, varTr * varNumVol, varTr)
        # Get supersampled frames times, i.e. start point of every volume in
        # upsampled res, since convolution takes place in temp. upsampled space
        vecFrmTms = np.arange(0, varTr * varNumVol, varTr / varTmpOvsmpl)

        # Convolving the best-fitting neural response with all hrf base fn
        aryMdlRsp = cnvl_nrl_hrf(vecNrlRsp, aryHrfBse, vecFrms, vecFrmTms,
                                 varTr, varNumVol)
#        aryMdlRsp = cnvl_nrl_hrf_vec(vecNrlRsp, aryHrfBse, vecFrms, vecFrmTms,
#                                     varTr, varNumVol)

        # Here would be space to implement a fit, for example checking if the
        # voxels time course fullfills specific crieteria.
        # For now just set lgcFit to True
        lgcFit = True

        # Only fit model if lgcFit:
        if lgcFit:

            # Check whether we need to crossvalidate
            if lgcXval:
                # We do crossvalidate. In this case, we loop through
                # the different folds of the crossvalidation and
                # calculate the cross-validation error for the current
                # model for all voxel time courses.

                # A cython function is used to calculate the residuals and
                # beta parameter estimates of the current model:
                if varNumFtr == 1:
                    # For time course with one predictors
                    aryResXval = cy_lst_sq_xval_one(aryMdlRsp.T,
                                                    aryFunc[:, idxVxl],
                                                    aryIdxTrn,
                                                    aryIdxTst)

                elif varNumFtr == 2:
                    # For time course with two predictors
                    if lgcPrint:
                        print('Cython currently not implemented for ' +
                              'time course with two predictors.')

                else:
                    if lgcPrint:
                        print('Cython currently not implemented for ' +
                              'more than two predictors.')

                # calculate the average cross validation error across
                # all folds
                vecTmpRes = np.mean(aryResXval, axis=1)

            else:
                # We do not crossvalidate. In this case, we calculate
                # the ratio of the explained variance (R squared)
                # for the current model for all voxel time courses.

                # A cython function is used to calculate the residuals and
                # beta parameter estimates of the current model:
                if varNumFtr == 1:
                    # For time course with one predictor
                    aryTmpBts, vecTmpRes = cy_lst_sq_one(aryMdlRsp.T,
                                                         aryFunc[:, idxVxl])

                elif varNumFtr == 2:
                    # For time course with two predictors
                    if lgcPrint:
                        print('Cython currently not implemented for ' +
                              'time course with two predictors.')
                else:
                    if lgcPrint:
                        print('Cython currently not implemented for ' +
                              'more than two two predictors.')

            # Collect residuals for this voxel for all models
            aryClcRes[idxVxl, :] = vecTmpRes

            # Get index for the winner model
            idxWnrMdl = np.argmin(vecTmpRes)

            # Replace best hrf parameters:
            vecBstPrm[idxVxl, :] = aryPrm[idxWnrMdl, :]

            # Replace best mean residual values:
            vecBstRes[idxVxl] = vecTmpRes[idxWnrMdl]

            if not lgcXval:
                # Replace best beta values:
                aryBstBts[idxVxl, :] = aryTmpBts[:, idxWnrMdl].T

            # In case we cross-validate we also save and replace the best
            # residual values for every fold (not only mean across folds):
            if lgcXval:
                aryBstResFlds[idxVxl, :] = aryResXval[idxWnrMdl, :]

        # Status indicator (only used in the first of the parallel
        # processes):
        if idxPrc == 0:

            # Increment status indicator counter:
            varCntSts02 = varCntSts02 + 1

    # After finding the best fitting model for each voxel, we still have to
    # calculate the average correlation coefficient between predicted and
    # measured time course (xval=True) or the coefficient of determination
    # (xval=False) for each voxel.

    if lgcXval:

        # Since we did not do this during finding the best model, we still need
        # to calculate deviation from a mean model for every voxel and fold
        # arySsTotXval as well as calculate the best betas for the full model

        # Calculate deviation from a mean model for every voxel and fold
        arySsTotXval = np.zeros((aryBstResFlds.shape),
                                dtype=aryBstResFlds.dtype)

        # Loop over all best-fitting model parameter combinations found
        for indPrm, vecPrm in enumerate(vecBstPrm):
            # Get voxel time course
            aryVxlTc = aryFunc[:, indPrm]
            # Get nerual model time courses
            aryNrlTmp = aryNrlRsp[indPrm, :]
            # Get hrf basis function based on best hrf params for this voxel
            aryHrfTmp = cvrt_hrf_prm_fn(np.atleast_2d(vecPrm), spm_hrf_compat,
                                        varTr, varTmpOvsmpl)
            # Create model time course
            aryMdlTc = cnvl_nrl_hrf_vec(aryNrlTmp, aryHrfTmp, vecFrms,
                                        vecFrmTms, varTr, varNumVol)

            # Calculate beta parameter estimates for entire model
            aryBstBts[indPrm, :] = np.linalg.lstsq(aryMdlTc.T,
                                                   aryVxlTc,
                                                   rcond=-1)[0]

            # loop over cross-validation folds
            for idxXval in range(varNumXval):
                # Get functional data for tst:
                aryFuncTst = aryVxlTc[aryIdxTst[:, idxXval]]
                # Deviation from the mean for each datapoint:
                aryFuncDev = np.subtract(aryFuncTst,
                                         np.mean(aryFuncTst,
                                                 axis=0))
                # Sum of squares:
                vecSsTot = np.sum(np.power(aryFuncDev, 2.0), axis=0)
                arySsTotXval[indPrm, idxXval] = vecSsTot

        # Calculate coefficient of determination by comparing:
        # aryBstResFlds vs. arySsTotXval

        # get logical to check that arySsTotXval is greater than zero in all
        # voxels and folds
        lgcExclZeros = np.all(np.greater(arySsTotXval,  np.array([0.0])),
                              axis=1)
        if lgcPrint:
            print('------------Nr of voxels: ' + str(len(lgcExclZeros)))
            print('------------Nr of voxels avove 0: ' +
                  str(np.sum(lgcExclZeros)))

        # Calculate R2 for every crossvalidation fold seperately
        aryBstR2fld = np.subtract(
            1.0, np.divide(aryBstResFlds,
                           arySsTotXval))

        # Calculate mean R2 across folds here
        vecBstR2 = np.subtract(
            1.0, np.mean(np.divide(aryBstResFlds,
                                   arySsTotXval),
                         axis=1))

        # Output list:
        lstOut = [idxPrc,
                  vecBstPrm,
                  vecBstR2,
                  aryBstBts,
                  aryClcRes,
                  aryBstR2fld]

        queOut.put(lstOut)

    else:
        # To calculate the coefficient of determination, we start with the
        # total sum of squares (i.e. the deviation of the data from the mean).
        # The mean of each time course:
        vecFuncMean = np.mean(aryFunc, axis=0)
        # Deviation from the mean for each datapoint:
        aryFuncDev = np.subtract(aryFunc, vecFuncMean[None, :])
        # Sum of squares:
        vecSsTot = np.sum(np.power(aryFuncDev,
                                   2.0),
                          axis=0)
        # Coefficient of determination:
        vecBstR2 = np.subtract(1.0,
                               np.divide(vecBstRes,
                                         vecSsTot))

        # Output list:
        lstOut = [idxPrc,
                  vecBstPrm,
                  vecBstR2,
                  aryBstBts,
                  aryClcRes]

        queOut.put(lstOut)
