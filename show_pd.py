
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu

# PH図を取得
dimension = 1
pd_moss = hc.PDList("output_for_vec/ph_results/3d_2000x_1-pd_moss.pdgm").dth_diagram(dimension)

# PH図を表示
pd_moss.histogram(x_bins=64).plot(colorbar={"type": "log"})
plt.savefig("pdimage_moss.png")
print(str(dimension)+"次のPH図を保存しました。")