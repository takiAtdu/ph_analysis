import os
import numpy as np
import matplotlib.pyplot as plt
import homcloud.interface as hc
import glob
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm

import common


condition = input("熱処理条件_倍率 : ")
phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range_min = int(input("pd_range_min : "))
pd_range_max = int(input("pd_range_max : "))
pd_range = (pd_range_min, pd_range_max)
diagonal = common.diagonal

pdnames = glob.glob("output/pdgm_"+phase+"/"+condition+"/*.pdgm")
pdnames.sort()

for pdname in pdnames:
    print(pdname)

# PH解析の結果を取得
pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

# ベクトル化
spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = "none")
pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

# 平均化
avg_vect = np.sum(pdvects, axis=0)
avg_vect /= len(pdnames)


print("描画開始")

spec.histogram_from_vector(avg_vect).plot(colorbar={"type": "log", "min": 1})

save_dir = "output/avgPD/"
os.makedirs(save_dir, exist_ok=True)
plt.savefig(save_dir + condition + "_" + phase + str(dimension) + ".png")
print(save_dir + condition + "_" + phase + str(dimension) + ".png")