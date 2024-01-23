import numpy as np
import matplotlib.pyplot as plt
import homcloud.interface as hc
import glob
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


labels = np.array(
        [
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 

        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 

        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
        ]
        )


phase = "moss"
dimension = 1
range = (-40, 40)
sigma = 1
weight = ("atan", 0.01, 10)


pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/for_vec/pdgm_"+phase+"/*.pdgm")
pdnames.sort()

for pdname in pdnames:
    print(pdname)

# PH解析の結果を取得
pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

# ベクトル化
spec = hc.PIVectorizeSpec(range, 64, sigma = sigma, weight = weight)
pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

# 正規化
print('pdvects (min, max) : (', pdvects.min(), ', ', pdvects.max(), ')')
pdvects = pdvects / pdvects.max()

print(pdvects[0].shape)

# 主成分解析
pca = PCA(n_components=10)
pca.fit(pdvects)

reduced = pca.transform(pdvects)



# # 寄与率を表示
# plt.bar([n for n in range(1, len(pca.explained_variance_ratio_)+1)], pca.explained_variance_ratio_)

# print([n for n in range(1, len(pca.explained_variance_ratio_)+1)])
# print(pca.explained_variance_ratio_)



# 主成分をプロット
x = []
y = []
z = []
for vec in reduced:
    x.append(vec[0])
    y.append(vec[1])
    z.append(vec[2])
x = x/max(x)
y = y/max(y)
z = z/max(z)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel("PC1", size = 10, color = "k")
ax.set_ylabel("PC2", size = 10, color = "k")
ax.set_zlabel("PC3", size = 10, color = "k")

ax.set_xticks([-1.0, -0.5, 0, 0.5, 1.0])
ax.set_yticks([-1.0, -0.5, 0, 0.5, 1.0])
ax.set_zticks([-1.0, -0.5, 0, 0.5, 1.0])


ax.scatter(x[labels == 1], y[labels == 1], z[labels == 1], s = 20, c = "k")
ax.scatter(x[labels == 2], y[labels == 2], z[labels == 2], s = 20, c = "r")
ax.scatter(x[labels == 3], y[labels == 3], z[labels == 3], s = 20, c = "b")
ax.scatter(x[labels == 4], y[labels == 4], z[labels == 4], s = 20, c = "y")
ax.scatter(x[labels == 5], y[labels == 5], z[labels == 5], s = 20, c = "g")
ax.scatter(x[labels == 6], y[labels == 6], z[labels == 6], s = 20, c = "c")

# ax.legend(['As Cast', '1600d1d', '1600d3d', '1600d3h', '1700d3h', '1800d3h'])

plt.show()

# 出力
plt.savefig("classification_" + phase + "_" + dimension + "_" + range[0] + "_" + range[1] + "_" + sigma + "_" + weight[0] + "_" + weight[1] + "_" + weight[2] + ".png")