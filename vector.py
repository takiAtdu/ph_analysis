import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu
import glob


dimension = 1
pd_tic = hc.PDList("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/ph_results/r1_1000x_1-pd_tic.pdgm").dth_diagram(dimension)
pd_t2_mo2c = hc.PDList("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/ph_results/r1_1000x_1-pd_t2.pdgm").dth_diagram(dimension)
pd_moss = hc.PDList("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/ph_results/r1_1000x_1-pd_moss.pdgm").dth_diagram(dimension)

spec = hc.PIVectorizeSpec((-40, 5), 128, sigma=31.5, weight=("atan", 0.01, 3))
pdvect = spec.vectorize(pd_tic)
print(pdvect)