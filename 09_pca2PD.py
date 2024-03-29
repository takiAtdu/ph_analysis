import os
import numpy as np
import matplotlib.pyplot as plt
import homcloud.interface as hc
import glob
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

import common


labels = np.array([1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100 + [6]*100)

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))

pc = int(input("第何主成分を解析しますか？ : "))

sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal

spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = weight)
pdvects = common.get_pdvects(phase, dimension)

# 正規化
print('pdvects (min, max) : (', pdvects.min(), ', ', pdvects.max(), ')')
pdvects = pdvects / pdvects.max()

print(pdvects[0].shape)

# 主成分解析
print("主成分分析中です。")
pca = PCA(n_components=10)
pca.fit(pdvects)


# 主成分をPDに戻す
# spec.histogram_from_vector(pca.mean_).plot()
if pc == 1:
    spec.histogram_from_vector(pca.components_[0, :]).plot(colorbar={"type":"linear-midpoint", "midpoint": 0})
elif pc == 2:
    spec.histogram_from_vector(pca.components_[1, :]).plot(colorbar={"type":"linear-midpoint", "midpoint": 0, "min": -0.8, "max": 0.8})
elif pc == 3:
    spec.histogram_from_vector(pca.components_[2, :]).plot(colorbar={"type":"linear-midpoint", "midpoint": 0, "min": -0.8, "max": 0.8})


# 出力
save_dir = "output/pca2PD/"
os.makedirs(save_dir, exist_ok=True)
plt.savefig(save_dir + "pca2PD_" + phase + str(dimension) +"_pc"+str(pc)+ ".png")