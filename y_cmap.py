import matplotlib.pyplot as plt
import pickle
import numpy as np
import glob
import homcloud.interface as hc

import common

phase = "moss"
dimension = 1
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal


X = []
Y = []
for i in range(64):
    x    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*i
    y = x
    x_dx = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(i+1)
    y_dy = x_dx

    X.append((x+x_dx)/2)
    Y.append((y+y_dy)/2)


print("係数取得開始")

model = 'model_reg_' + phase + str(dimension) + '.sav'
lss = pickle.load(open(model, 'rb'))

print("係数取得終了")


print("PDベクトル取得開始")

# pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/for_vec/pdgm_"+phase+"/*.pdgm")
pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/pdgm_"+phase+"/*.pdgm")
pdnames.sort()

for pdname in pdnames:
    print(pdname)

# PH解析の結果を取得
pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

# ベクトル化
spec = hc.PIVectorizeSpec(pd_range, 64, sigma = sigma, weight = weight)
pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

# 対角成分を削る
for pdvect in pdvects:
    for i in diagonal:
        pdvect[i] = 0
        pdvect[i-1] = 0

print("PDベクトル取得終了")


print("y算出開始")

# pdvectの平均値を求める
pdvect_mean = np.mean(pdvects, axis=0)
count = 0
Z = np.zeros((64, 64))
for i in range(64):
    for j in range(i+1):
        count += 1
        if lss.coef_[count-1] > 0:
            Z[i][j] = lss.coef_[count-1] * pdvect_mean[count-1]


count = 0
y_dict = {}
for i in range(64):
    for j in range(i+1):
        count += 1
        if lss.coef_[count-1] != 0:
            # print(count, "は", i+1, "行目, ", j+1, "列目で、値は", lss.coef_[count-1])

            x    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*j
            y    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*i
            x_dx = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(j+1)
            y_dy = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(i+1)

            y_dict[(x, y, x_dx, y_dy)] = lss.coef_[count-1] * pdvect_mean[count-1]
# effective_coef_list = sorted(effective_coef_dict.items(), key = lambda coef : abs(coef[1]), reverse=True)
y_list = sorted(y_dict.items(), key = lambda coef : coef[1], reverse=True)
print(y_list)


print("y算出終了")



XX, YY = np.meshgrid(X, Y)
ZZ = np.flipud(Z).copy()

print("描画開始")
# plt.figure()
# ax = plt.subplot(111)
# cs = ax.contourf(XX, YY, Z, 100, cmap='Reds')
# plt.colorbar(cs)
# plt.show()

# Xmin, Xmax, Ymin, Ymax
extent = (-40, 40, -40, 40)
plt.imshow(ZZ, cmap="Reds", extent=extent)

# 斜線
plt.plot([-40, 40],[-40, 40],color='black',linewidth=1)
# 縦線
for i in range(7):
  params = -30 + 10*i
  plt.plot([params, params],[-40, 40],color='gray',linewidth=0.5)
# 横線
for i in range(7):
  params = -30 + 10*i
  plt.plot([-40, 40],[params, params],color='gray',linewidth=0.5)


plt.colorbar()
plt.savefig("y_cmap_" + phase + str(dimension) + ".png")