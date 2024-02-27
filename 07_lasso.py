# https://helve-blog.com/posts/python/sklearn-lasso-regression/

import os
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import homcloud.interface as hc
import glob
import matplotlib.pyplot as plt
import pickle

import common

hv = common.get_hv()
# ["1600c24h", "1600c3h", "1700c3h", "1800c24h", "1800c3h", "As Cast"]

y = [hv[0]]*100 + [hv[1]]*100 + [hv[2]]*100 + [hv[3]]*100 + [hv[4]]*100 + [hv[5]]*100

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal


pdvects = common.get_pdvects(phase, dimension)
print("pdvects.shape: ", pdvects.shape)


X = pdvects
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

lss = Lasso(alpha=0.1)
lss.fit(X_train, y_train)

save_dir = "output/lasso/"
os.makedirs(save_dir, exist_ok=True)
filename = phase + str(dimension) + ".sav"
pickle.dump(lss, open(save_dir+filename, 'wb'))

y_pred = lss.predict(X_test)

print('train score: ', lss.score(X_train, y_train))
print('test score: ', lss.score(X_test, y_test))

print('元の特徴量の数: ', X.shape[1])
print('Lasso の特徴量: ', np.sum(lss.coef_ != 0))

print('最小2乗誤差: ', mean_squared_error(y_test,y_pred))


result_1600c24h = []
result_1600c3h = []
result_1700c3h = []
result_1800c3h = []
result_1800c24h = []
result_ascast = []
for i in range(len(y_test)):
    if y_test[i] == hv[0]:
        result_1600c24h.append(y_pred[i])
    elif y_test[i] == hv[1]:
        result_1600c3h.append(y_pred[i])
    elif y_test[i] == hv[2]:
        result_1700c3h.append(y_pred[i])
    elif y_test[i] == hv[3]:
        result_1800c24h.append(y_pred[i])
    elif y_test[i] == hv[4]:
        result_1800c3h.append(y_pred[i])
    elif y_test[i] == hv[5]:
        result_ascast.append(y_pred[i])

avg_1600c24h = sum(result_1600c24h)/len(result_1600c24h)
print('1600c24hの平均値: ', avg_1600c24h)

avg_1600c3h = sum(result_1600c3h)/len(result_1600c3h)
print('1600c3hの平均値: ', avg_1600c3h)

avg_1700c3h = sum(result_1700c3h)/len(result_1700c3h)
print('1700c3hの平均値: ', avg_1700c3h)

avg_1800c24h = sum(result_1800c24h)/len(result_1800c24h)
print('1800c24hの平均値: ', avg_1800c24h)

avg_1800c3h = sum(result_1800c3h)/len(result_1800c3h)
print('1800c3hの平均値: ', avg_1800c3h)

avg_ascast = sum(result_ascast)/len(result_ascast)
print('ascastの平均値: ', avg_ascast)


plt.scatter(y_pred, y_test, s = 20, c = "b")
plt.scatter(avg_1600c24h, hv[0], s = 20, c = "r")
plt.scatter(avg_1600c3h,  hv[1], s = 20, c = "r")
plt.scatter(avg_1700c3h,  hv[2], s = 20, c = "r")
plt.scatter(avg_1800c24h, hv[3], s = 20, c = "r")
plt.scatter(avg_1800c3h,  hv[4], s = 20, c = "r")
plt.scatter(avg_ascast,   hv[5], s = 20, c = "r")
plt.xlabel("predicted")
plt.ylabel("measured")

plt.savefig(save_dir + str(phase) + str(dimension) + ".png")
# plt.show()