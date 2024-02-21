import numpy as np
import matplotlib.pyplot as plt
import homcloud.interface as hc
import glob
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm

import common

labels = np.array([1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100 + [6]*100)

condition = input("熱処理条件 : ")

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal

pdnames = glob.glob("output/pdgm_"+phase+"/"+condition+"*.pdgm")
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
avg_vect /= 100


print("描画開始")

spec.histogram_from_vector(avg_vect).plot(colorbar={"type": "log", "min": 1})

plt.savefig("avg_pd_" + condition + "_" + phase + str(dimension) + ".png")