import sys
sys.path.append('../config/')
from imports import *
from settings import *
from advanced_settings import *

sys.path.append('../lib/')
import ANA_lib
import aux_lib
import derived_predictors
import down_scene_ANA
import down_scene_MOS
import down_scene_RAW
import down_scene_TF
import down_scene_WG
import down_day
import down_point
import evaluate_methods
import grids
import launch_jobs
import MOS_lib
import plot
import postpro_lib
import postprocess
import precontrol
import preprocess
import process
import read
import transform
import TF_lib
import val_lib
import WG_lib
import write


########################################################################################################################
def down_day(targetVar, pred_scene, saf_scene, var_scene, pred_calib, saf_calib, var_calib, obs, corr, coef, intercept,
             centroids, i_4nn, j_4nn, w_4nn, methodName):

    # Creates empty array for results
    est = np.zeros((hres_npoints[targetVar]))

    # Define analogy_mode and estimation_mode
    if methodName not in ('MLR-ANA', 'MLR-WT'):
        analogy_mode = methodName.split('-')[1]
        estimation_mode = methodName.split('-')[2]

    special_value = int(100 * predictands_codification[targetVar]['special_value'])

    # Adds axis so scene and calib have the same dimensions
    saf_scene = saf_scene[np.newaxis,:]

    # Gets synoptic analogs and theis synoptic distances
    syn_dist = ANA_lib.get_synoptic_distances(saf_calib, saf_scene)

    # Checks for missing predictands
    valid = np.where(obs < special_value)[0]
    dist_th = np.sort(syn_dist)[kNN]

    # Gets weather type id and dist to centroid only if using clusters
    if methodName == 'MLR-WT':
        weather_type = ANA_lib.get_weather_type_id(saf_scene, centroids)
        dist_centroid = weather_type['dist']
        weather_type_id = weather_type['k_index']
    else:
        weather_type = None
        dist_centroid = None
        weather_type_id = None

    if methodName in ('MLR-ANA', 'MLR-WT'):
        # Adds axis so scene and calib have the same dimensions
        pred_scene = pred_scene[np.newaxis, :, :, :]
        iana = np.argsort(syn_dist)[:n_analogs_preselection]

        # Goes through high resolution grid
        for ipoint in range(hres_npoints[targetVar]):
            if methodName == 'MLR-WT':
                coef_ipoint = coef[weather_type_id, ipoint]
                intercept_ipoint = intercept[weather_type_id, ipoint]
            else:
                coef_ipoint = None
                intercept_ipoint = None

            # Downscale point
            est[ipoint] = down_point.ANA_others(targetVar, iana, pred_scene, var_scene, pred_calib, var_calib, obs[:, ipoint],
                                           coef_ipoint,
                                           intercept_ipoint, dist_centroid, i_4nn[ipoint], j_4nn[ipoint],
                                           w_4nn[ipoint], methodName)


    else:
        # If mode synop and no missing predictands, downsale at daily level
        if ((analogy_mode in ['SYN', 'VAR']) and (valid.size == obs.size)):
            if (estimation_mode == '1NN'):
                est = obs[np.argmin(syn_dist)]
            else:
                obs = obs[syn_dist <= dist_th]
                syn_dist = syn_dist[syn_dist <= dist_th]
                syn_dist[syn_dist == 0] = 0.000000001
                W = np.ones(syn_dist.shape) / syn_dist
                # Estimates precipitation with one decimal
                if estimation_mode == 'kNN':
                    est = np.average(obs, weights=W, axis=0)
                elif estimation_mode == 'rand':
                    i = np.random.choice(np.arange(W.size), p=W/np.nansum(W))
                    est = obs[i]

        # Downscale at point level
        else:
            if pred_scene is not None:
                # Adds axis so scene and calib have the same dimensions
                pred_scene = pred_scene[np.newaxis, :, :, :]

            # Gets "n_analogs_preselection" (150) synoptic analogs and theis synoptic distances
            iana = np.argsort(syn_dist)[:n_analogs_preselection]
            syn_dist = syn_dist[iana]

            if analogy_mode == ('LOC'):
                # Gets weather type id and dist to centroid
                weather_type = ANA_lib.get_weather_type_id(saf_scene, centroids)
                weather_type_id = weather_type['k_index']
            else:
                weather_type_id = None

            # Goes through high resolution grid
            for ipoint in range(hres_npoints[targetVar]):

                if analogy_mode == ('LOC'):
                    corr_ipoint = corr[:,ipoint]
                else:
                    corr_ipoint = None

                # Downscale point
                est[ipoint] = down_point.ANA_pr(syn_dist, weather_type_id, iana, pred_scene, var_scene, pred_calib,
                                                  var_calib, obs[:,ipoint], corr_ipoint, i_4nn[ipoint], j_4nn[ipoint],
                                                  w_4nn[ipoint], methodName, special_value)

    return est

