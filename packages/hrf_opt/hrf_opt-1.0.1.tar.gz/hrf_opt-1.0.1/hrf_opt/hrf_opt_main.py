# -*- coding: utf-8 -*-
"""Optimize the hrf parameters, given estimated pRF parameters."""

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


import time
import os
import numpy as np
import multiprocessing as mp

from hrf_opt.load_config import load_config
from hrf_opt.hrf_opt_utils import cls_set_config, crt_hrf_prm, cvrt_hrf_prm_fn
from hrf_opt.find_opt_hrf import find_opt_hrf

from pyprf_feature.analysis.utils_general import (load_res_prm, joinRes,
                                                  export_nii)
from pyprf_feature.analysis.prepare import prep_func
from pyprf_feature.analysis.model_creation_utils import crt_nrl_tc
from pyprf_feature.analysis.utils_hrf import spm_hrf_compat

###### DEBUGGING ###############
#strCsvCnfg = "/home/marian/Documents/Testing/pyprf_feature_devel/control/S02_config_motDepPrf_flck_smooth_inw_hrf_opt.csv"
#lgcTest = False
################################


def hrf_opt_run(strCsvCnfg, lgcTest=False):
    """
    Main function for hrf_opt.

    Parameters
    ----------
    strCsvCnfg : str
        Absolute file path of config file.
    lgcTest : Boolean
        Whether this is a test (pytest). If yes, absolute path of pyprf libary
        will be prepended to config file paths.

    """

    # %% Preparations

    # Check time
    print('---pRF analysis')
    varTme01 = time.time()

    # Load config parameters from csv file into dictionary:
    dicCnfg = load_config(strCsvCnfg, lgcTest=lgcTest)

    # Load config parameters from dictionary into namespace:
    cfg = cls_set_config(dicCnfg)

    # If suppressive surround flag is on, make sure to retrieve results from
    # that fitting
    if cfg.lgcSupsur:
        cfg.strPathOut = cfg.strPathOut + '_supsur'

    # Convert preprocessing parameters (for temporal smoothing)
    # from SI units (i.e. [s]) into units of data array (volumes):
    cfg.varSdSmthTmp = np.divide(cfg.varSdSmthTmp, cfg.varTr)

    # Check whether we need to crossvalidate
    if np.greater(cfg.varNumXval, 1):
        cfg.lgcXval = True
    elif np.equal(cfg.varNumXval, 1):
        cfg.lgcXval = False
    strErrMsg = 'Stopping program. ' + \
        'Set numXval (number of crossvalidation folds) to 1 or higher'
    assert np.greater_equal(cfg.varNumXval, 1), strErrMsg

    # %% Load empirical voxel time courses and pRF models from first fit

    # Load the empirical voxel time courses
    # Some voxels were excluded because they did not have sufficient mean
    # and/or variance - exclude their initial parameters, too
    # Get inclusion mask and nii header
    aryLgcMsk, aryLgcVar, hdrMsk, aryAff, aryFunc, tplNiiShp = prep_func(
        cfg.strPathNiiMask, cfg.lstPathNiiFunc, varAvgThr=-100)

    # Derive path to R2 results from first fit
    lstR2Path = [cfg.strPathFitRes + '_R2.nii.gz']
    # Check if fitting has been performed, i.e. whether R2 file exists
    # Throw error message if it does not exist.
    errorMsg = 'Files that should have resulted from fitting do not exist. \
                \nPlease perform pRF fitting first, calling  e.g.: \
                \npyprf_feature -config /path/to/my_config_file.csv'
    # Check if fitting has been performed, i.e. whether parameter file exists
    assert os.path.isfile(lstR2Path[0]), errorMsg
    # Load the R2 parameters from first fit
    vecR2 = load_res_prm(lstR2Path, lstFlsMsk=[cfg.strPathNiiMask])[0][0]
    # Make sure that R2 is one-dimensional
    vecR2 = np.squeeze(vecR2)
    # Apply inclusion mask to vecR2
    vecR2 = vecR2[aryLgcVar]

    # Derive path to aperture responses for winner model from first fit
    lstMdlRspPath = [cfg.strPathFitRes + '_FitMdlRsp.nii.gz']
    # Check if winner model responses to aperture conditions have been saved,
    # i.e. pyprf_feature was run with -save_tc -mdl_rsp flags after fitting
    errorMsg = 'Files that should have resulted from fitting do not exist. \
                \nPlease perform pRF fitting first, then call to \
                pyprf_feature with the -save_tc and -mdl_rsp flags: \
                \npyprf_feature -config /path/to/config.csv -save_tc -mdl_rsp'
    # Check if fitting has been performed, i.e. whether response file exists
    assert os.path.isfile(lstMdlRspPath[0]), errorMsg
    # Load response to apertures for each voxel for winner model from first fit
    lstMdlRspPath = [cfg.strPathFitRes + '_FitMdlRsp.nii.gz']
    aryMdlRsp = load_res_prm(lstMdlRspPath,
                             lstFlsMsk=[cfg.strPathNiiMask])[0][0]
    # Apply inclusion mask to aryMdlRsp
    aryMdlRsp = aryMdlRsp[aryLgcVar, :]

    # Obtain a mask for voxel inclusion by thresholding with R2 value
    aryLgcR2 = np.greater(vecR2, cfg.varThrR2)
    # Apply the R2 mask to aryFunc and aryMdlRsp
    aryFunc = aryFunc[aryLgcR2, :]
    aryMdlRsp = aryMdlRsp[aryLgcR2, :]
    # Apply the R2 mask to voxel inclusion mask
    aryLgcVar[aryLgcVar] = aryLgcR2

    # %% Prepare hrf base functions and predicted neural time courses

    # Print statement to user
    print('---Create predicted neural responses')

    # Create hrf parameter combinations
    aryPrm = crt_hrf_prm(cfg.varPkDelMin, cfg.varPkDelMax,
                         cfg.varUndDelMin, cfg.varUndDelMax,
                         cfg.varDelStp, cfg.varPkDspMin, cfg.varPkDspMax,
                         cfg.varUndDspMin, cfg.varUndDspMax, cfg.varDspStp,
                         cfg.varPkUndRatMin, cfg.varPkUndRatMax,
                         cfg.varPkUndRatStp)

    # create hrf base functions for each of the model parameter combinations
    aryHrfBse = cvrt_hrf_prm_fn(aryPrm, spm_hrf_compat, cfg.varTr,
                                cfg.varTmpOvsmpl)
    # Exclude hrf basis functions that have any NaN values
    lgcNan = np.any(np.isnan(aryHrfBse), axis=1)
    aryHrfBse = aryHrfBse[np.invert(lgcNan), :]
    if np.any(lgcNan):
        print('------Nan values detected & ecluded in basis hrf functions')

    # Load temporal information about when which apertures was presented in the
    # experiment
    aryTmpExpInf = np.load(cfg.strTmpExpInf)

    # Create predicted neural response for model in question
    aryNrlRsp = crt_nrl_tc(aryMdlRsp, aryTmpExpInf[:, 0], aryTmpExpInf[:, 1],
                           aryTmpExpInf[:, 2], cfg.varTr, cfg.varNumVol,
                           cfg.varTmpOvsmpl)

    # free some memory
    del(aryTmpExpInf)
    del(aryMdlRsp)

    # %% Optimize the hrf function

    # Empty list for results (parameters of best fitting pRF model):
    lstPrfRes = [None] * cfg.varPar

    # Empty list for processes:
    lstPrcs = [None] * cfg.varPar

    # Create a queue to put the results in:
    queOut = mp.Queue()

    # Print statement to user
    print('---Optimization will be performed on this number of voxels: ' +
          str(aryFunc.shape[0]))
    print('---Optimization will be performed on this number of models: ' +
          str(aryPrm.shape[0]))

    # Create list with chunks of functional data for the parallel processes:
    lstFunc = np.array_split(aryFunc, cfg.varPar)
    # Create list with chunks of aryNrlRsp for the parallel processes:
    lstNrlRsp = np.array_split(aryNrlRsp, cfg.varPar)

    # We don't need the original array with the functional data anymore:
    del(aryFunc)
    del(aryNrlRsp)

    print('------Optimize hrf functions')

    # Create processes:
    for idxPrc in range(0, cfg.varPar):
        lstPrcs[idxPrc] = mp.Process(target=find_opt_hrf,
                                     args=(idxPrc,
                                           lstFunc[idxPrc].T,
                                           lstNrlRsp[idxPrc],
                                           aryHrfBse,
                                           aryPrm,
                                           cfg.varTr,
                                           cfg.varNumVol,
                                           cfg.varTmpOvsmpl,
                                           cfg.lgcXval,
                                           cfg.varNumXval,
                                           queOut),
                                     )
        # Daemon (kills processes when exiting):
        lstPrcs[idxPrc].Daemon = True

    # Start processes:
    for idxPrc in range(0, cfg.varPar):
        lstPrcs[idxPrc].start()

    # Delete reference to list with function data (the data continues to exists
    # in child process):
    del(lstFunc)

    # Collect results from queue:
    for idxPrc in range(0, cfg.varPar):
        lstPrfRes[idxPrc] = queOut.get(True)

    # Join processes:
    for idxPrc in range(0, cfg.varPar):
        lstPrcs[idxPrc].join()

    # %% Prepare pRF finding results for export

    # Put output into correct order:
    lstPrfRes = sorted(lstPrfRes)

    # collect results from parallelization
    aryBstPrm = joinRes(lstPrfRes, cfg.varPar, 1, inFormat='2D')
    aryBstR2 = joinRes(lstPrfRes, cfg.varPar, 2, inFormat='1D')
    aryBstBts = joinRes(lstPrfRes, cfg.varPar, 3, inFormat='2D')
    aryAllRes = joinRes(lstPrfRes, cfg.varPar, 4, inFormat='2D')
    if np.greater(cfg.varNumXval, 1):
        aryBstR2Single = joinRes(lstPrfRes, cfg.varPar, 5, inFormat='2D')

    # Delete unneeded large objects:
    del(lstPrfRes)

    # %% Save results to disk:

    # List with name suffices of output images:
    lstNiiNames = ['_R2']

    # Create full path names from nii file names and output path
    lstNiiNames = [cfg.strPathOut + strNii + '.nii.gz' for strNii in
                   lstNiiNames]

    # export beta parameter as a single 4D nii file
    export_nii(np.atleast_2d(aryBstR2).T, lstNiiNames, aryLgcMsk, aryLgcVar,
               tplNiiShp, aryAff, hdrMsk, outFormat='3D')

    # List with name suffices of output images:
    lstNiiNames = ['_HrfPrm']

    # Create full path names from nii file names and output path
    lstNiiNames = [cfg.strPathOut + strNii + '.nii.gz' for strNii in
                   lstNiiNames]

    # export beta parameter as a single 4D nii file
    export_nii(aryBstPrm, lstNiiNames, aryLgcMsk, aryLgcVar, tplNiiShp,
               aryAff, hdrMsk, outFormat='4D')

    # List with name suffices of output images:
    lstNiiNames = ['_Betas']

    # Create full path names from nii file names and output path
    lstNiiNames = [cfg.strPathOut + strNii + '.nii.gz' for strNii in
                   lstNiiNames]

    # export beta parameter as a single 4D nii file
    export_nii(aryBstBts, lstNiiNames, aryLgcMsk, aryLgcVar, tplNiiShp,
               aryAff, hdrMsk, outFormat='4D')

    if np.greater(cfg.varNumXval, 1):

        # truncate extremely negative R2 values
        aryBstR2Single[np.where(np.less_equal(aryBstR2Single, -1.0))] = -1.0

        # List with name suffices of output images:
        lstNiiNames = ['_R2_single']

        # Create full path names from nii file names and output path
        lstNiiNames = [cfg.strPathOut + strNii + '.nii.gz' for strNii in
                       lstNiiNames]

        # export R2 maps as a single 4D nii file
        export_nii(aryBstR2Single, lstNiiNames, aryLgcMsk, aryLgcVar,
                   tplNiiShp, aryAff, hdrMsk, outFormat='4D')

    # %% Save global winner hrf parameter combinations

    # Save the hrf parameter combination that minimizes across all voxels
    arySumRes = np.sum(aryAllRes, axis=0)
    vecMinPrm = aryPrm[np.argmin(arySumRes, axis=0), :]
    np.save(cfg.strPathOut + '_minHrfPrm', vecMinPrm)

    # Save the average hrf parameter combination across all voxels
    vecAvgPrm = np.mean(aryBstPrm, axis=0)
    np.save(cfg.strPathOut + '_avgHrfPrm', vecAvgPrm)

    # %% Report time

    varTme02 = time.time()
    varTme03 = varTme02 - varTme01
    print('---Elapsed time: ' + str(varTme03) + ' s')
    print('---Done.')
