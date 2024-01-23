# https://helve-blog.com/posts/python/sklearn-lasso-regression/

import matplotlib.pyplot as plt
import pickle
import numpy as np

phase = "moss"
dimension = 1
pd_range = (-40, 40)
bins = 64
sigma = 1
weight = ("atan", 0.01, 10)


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

model = 'model_reg.sav'
lss = pickle.load(open(model, 'rb'))

count = 0
Z = np.zeros((64, 64))
for i in range(64):
    for j in range(i+1):
        count += 1
        if lss.coef_[count-1] > 0:
            Z[i][j] = lss.coef_[count-1]

print("係数取得終了")

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
plt.imshow(ZZ, cmap="Greys", extent=extent)

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
plt.savefig("coef_cmap_" + phase + str(dimension) + ".png")