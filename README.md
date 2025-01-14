# pyClim-SDM: Statistical Downscaling for Climate Change Projections with a Graphical User Interface  

<br/><br/>
![](doc/pyClim-SDM_demo.gif)
<br/><br/>

**Institution:** Spanish Meteorological Agency (AEMET)

**License:** GNU General Public License v3.0

**Citation:** Hernanz, A., Correa, C., García-Valero, J. A., Domínguez, M., Rodríguez-Guisado, E., & Rodríguez-Camino, E. (2023). pyClim-SDM: Service for generation of statistical downscaled climate change projections supporting national adaptation strategies. Climate Services. https://doi.org/10.1016/j.cliser.2023.100408
___

pyClim-SDM is a software for statistical downscaling of climate change projections for the following daily surface variables: mean, maximum and minimum temperature, precipitation, zonal and meridional wind components, relative and specific humidity, cloud cover, surface downwelling shortwave and longwave radiation, evaporation, potential evaporation, sea level pressure, surface pressure, total runoff and soil water content.
Additionally, it is prepared for downscaling any other user defined variable. pyClim-SDM incorporates the following utilities:
- evaluation of Global Climate Models (GCMs).
- downscaling of both reanalysis (for evaluation) and GCMs.
- bias correction of downscaled climate projections.
- post-processing: ETCCDI extreme climate indices (Karl *et al*., 1999; https://www.climdex.org/learn/indices/).
- visualization of downscaled projections and evaluation metrics.


# Methods

### Raw:
- **RAW**: no downscaling (nearest grid point).
- **RAW-BIL**: no downscaling (bilinear interpolation).
### Model Output Statistics:
- **QM**: Empirical Quantile Mapping (Themeßl *et al*., 2011).
- **DQM**: Detrended Quantile Mapping (Cannon *et al.*, 2015). Quantile adjustment over detrended series.
- **QDM**: Quantile Delta Mapping in (Cannon *et al.*, 2015). Delta change over quantiles.
- **PSDM**: (Parametric) Scaled Distribution Mapping (Switanek *et al.*, 2017).
### Analogs / Weather Typing:
- **ANA-SYN**: Analog based on synoptic analogy. **1NN**: Nearest analog, **kNN**: k-nearest analogs, **rand**: random analog from Probability Density Function. See Hernanz *et al.* (2021).
- **ANA-LOC**: Same as ANA-SYN but using synoptic+local analogy. See Petisco de Lara, (2008a), Amblar-Francés *et al*. (2017) and Hernanz *et al.* (2021).
- **ANA-VAR**: Same as ANA-SYN but using the spatial pattern of the target variable itself.
### Linear:
- **MLR**: multiple linear regression. See Amblar-Francés *et al*., (2017) and Hernanz *et al.* (2021). Based on SDSM (Wilby *et al.*, 2002).
- **MLR-ANA**: multiple linear regression based on analogs. See Petisco de Lara (2008b), Amblar-Francés *et al*. (2017) and Hernanz *et al.* (2021).
- **MLR-WT**: multiple linear regression based on weather types. Similar to ANA-MLR but using precalibrated relationships for each weather type.
- **GLM**: Generalized Linear Model. Logistic + MLR (**LIN**), or over transformed data (**EXP** for exponential and **CUB** for cubic regression). See Amblar-Francés *et al*. (2017) and Hernanz *et al.* (2021). Based on SDSM (Wilby *et al.*, 2002).
### Machine Learning:
- **SVM**: Support Vector Machine. Non-linear machine learning classification/regression. See Hernanz *et al.* (2021).
- **LS-SVM**: Least Square Support Vector Machine. Non-linear machine learning classification/regression. See Hernanz *et al.* (2021).
- **RF**: Random Forest. Non-linear machine learning classification/regression. This method is combined with a MLR to extrapolate to values out of the observed range (configurable).
- **XGB**: eXtreme Gradient Boost. Non-linear machine learning classification/regression. This method is combined with a MLR to extrapolate to values out of the observed range (configurable).
- **ANN**: Artificial Neural Networks. Non-linear machine learning classification/regression. See García-Valero (2021) and Hernanz *et al.* (2021).
- **CNN**: Convolutional Neural Networks. Non-linear machine learning classification/regression. 
### Weather Generators:
- **WG-PDF**: Downscaling parameters of the distributions instead of downscaling daily data. See Erlandsen *et al.* (2020) and Benestad (2021).
- **WG-NMM**: Non-homogeneous Markov Model. Non-parametric Weather Generator based on a first-order two-state (wet/dry) Markov chain. Both the transition probabilities and the empirical distributions used for the intensity are conditioned on the precipitation given by the reanalysis/models. See Richardson (1981).



# Installation

pyClim-SDM has been originally designed for **Linux** and might present problems over a different OS.

In order to use pyClim-SDM, **python3** is required. pyClim-SDM makes use of the python libaries listed at 
requirements.txt. You can install them by following these steps: 
- Install Miniconda 3 (6Gb aprox. needed): https://docs.conda.io/en/latest/miniconda.html
- Create a virtual environment: **conda create -n env_pyClim-SDM -y -c conda-forge absl-py=1.2.0 numpy=1.23.1 pandas=1.4.3 geopandas=0.7.0 geopy=2.2.0 matplotlib=3.5.2 mpi4py=3.1.3 netCDF4=1.6.0 scikit-learn=1.1.2 scipy=1.9.0 seaborn=0.11.2 Shapely=1.8.2 statsmodels=0.13.2 tensorflow=2.7.0 xarray=0.17.0 xgboost=1.5.1 basemap=1.3.3 xarray**
- Activate your environment: **conda activate env_pyClim-SDM**


# References
 
- Amblar-Francés, P., Casado-Calle, M.J., Pastor-Saavedra, M.A., Ramos-Calzado, P., and Rodríguez-Camino, E. (2017). Guía de escenarios regionalizados de cambio climático sobre España a partir de los resultados del IPCC-AR5. Available at: https://www.aemet.es/documentos/es/conocermas/recursos_en_linea/publicaciones_y_estudios/publicaciones/Guia_escenarios_AR5/Guia_escenarios_AR5.pdf

- Benestad, R.E. (2021) A Norwegian approach to downscaling. Geoscientific Model Development Discussion (in review). https://doi.org/10.5194/gmd-2021-176. 

- Cannon, A.J., S.R. Sobie, and T.Q. Murdock (2015). Bias Correction of GCM Precipitation by Quantile Mapping: How Well Do Methods Preserve Changes in Quantiles and Extremes?. J. Climate, 28, 6938–6959, https://doi.org/10.1175/JCLI-D-14-00754.1

- Erlandsen, H.B., Parding, K.M., Benestad, R., Mezghani, A. and Pontoppidan, M. (2020). A hybrid downscaling approach for future temperature and precipitation change. Journal of Applied Meteorology and Climatology, 59(11), 1793–1807. https://doi.org/10.1175/JAMC-D-20-0013.1

- García-Valero, J.A. (2021). Redes neuronales artificiales. Aplicación a la regionalización de la precipitación y temperaturas diarias. In: AEMET Nota Técnica, Área de Evaluación y Modelización del Cambio Climático. Spain: AEMET. https://www.aemet.es/documentos/es/conocermas/recursos_en_linea/publicaciones_y_estudios/publicaciones/NT_34_Redes_neuronales_artificiales/NT_34_Redes_neuronales_artificiales.pdf

- Hernanz, A., García-Valero, J. A., Domínguez, M., Ramos-Calzado, P., Pastor-Saavedra, M. A. and Rodríguez-Camino, E. (2021). Evaluation of statistical downscaling methods for climate change projections over Spain: present conditions with perfect predictors. International Journal of Climatology, 42( 2), 762– 776. https://doi.org/10.1002/joc.7271

- Karl, T.R., Nicholls, N., Ghazi, A. (1999). CLIVAR/GCOS/WMO workshop on indices and indicators for climate extremes. Workshop summary. Climatic Change 42, 3–7. https://doi.org/10.1007/978-94-015-9265-9_2

- Petisco de Lara, S.E. (2008a). Método de regionalización de precipitación basado en análogos. Explicación y Validación. In: AEMET Nota Técnica 3A, Área de Evaluación y Modelización del Cambio Climático. Spain: AEMET. 

- Petisco de Lara, S.E. (2008b). Método de regionalización de temperatura basado en análogos. Explicación y Validación. In: AEMET Nota Técnica 3B, Área de Evaluación y Modelización del Cambio Climático. Spain: AEMET.

- Richardson, C. W. (1981), Stochastic simulation of daily precipitation, temperature, and solar radiation, Water Resour. Res., 17( 1), 182– 190, https://doi.org/10.1029/WR017i001p0018

- Switanek, M.B., Troch, P.A., Castro, C.L., Leuprecht, A., Chang, H.-I., Mukherjee, R., and Demaria, E.M.C. (2017). Scaled distribution mapping: a bias correction method that preserves raw climate model projected changes, Hydrol. Earth Syst. Sci., 21, 2649–2666, https://doi.org/10.5194/hess-21-2649-2017

- Themeßl, M.J., Gobiet, A. and Leuprecht, A. (2011). Empirical-statistical downscaling and error correction of daily precipitation from regional climate models. Int. J. Climatol., 31: 1530-1544. https://doi.org/10.1002/joc.2168

- Wilby, R., Dawson, C. and Barrow, E.M. (2002). SDSM—a decision support tool for the assessment of regional climate change impacts. Environmental Modelling & Software, 17, 145–157. https://doi.org/10.1016/S1364-8152(01)00060-3


