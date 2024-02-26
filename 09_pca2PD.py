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


# pdnames = glob.glob("output/pdgm_"+phase+"/*.pdgm")
# pdnames.sort()

# for pdname in pdnames:
#     print(pdname)

# print("上記のpdgmファイルを読み込んでいます。")

# # PH解析の結果を取得
# pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]


# print("ベクトル化しています。")
# # ベクトル化
# spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = weight)
# pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = weight)
pdvects_list = glob.glob("output/vectorize/*.txt")
for i in range(len(pdvects_list)):
    if i == 0:
        pdvects = pdvects_list[i]
    else:
        pdvects = np.concatenate([pdvects, pdvects_list[i]])

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
plt.savefig("pca2PD_" + phase + str(dimension) +"_pc"+str(pc)+ ".png")