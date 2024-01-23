# https://helve-blog.com/posts/python/sklearn-lasso-regression/

import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import homcloud.interface as hc
import glob
import matplotlib.pyplot as plt
import pickle


y = [
    1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 
    1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 

    1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 
    1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 

    1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 
    1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 1800, 
    ]


phase = "moss"
dimension = 1
pd_range = (-40, 40)
bins = 64
sigma = 1
weight = ("atan", 0.01, 10)


pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/for_vec/pdgm_"+phase+"/*.pdgm")
pdnames.sort()

# PH解析の結果を取得
pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

# ベクトル化
spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = weight)
pdvects = np.vstack([spec.vectorize(pd) for pd in pds])

print('pdvects (min, max) : (', pdvects.min(), ', ', pdvects.max(), ')')
# pdvects = pdvects / pdvects.max()

pca = PCA(n_components=10)
pca.fit(pdvects)

reduced = pca.transform(pdvects)

X = pdvects

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

lss = Lasso(alpha=0.1)
lss.fit(X_train, y_train)

filename = 'model_reg_' + phase + str(dimension) + '.sav'
pickle.dump(lss, open(filename, 'wb'))

y_pred = lss.predict(X_test)

print('train score : ', lss.score(X_train, y_train))
print('test score : ', lss.score(X_test, y_test))

print('元の特徴量の数 : ', X.shape[1])
print('Lasso の特徴量 : ', np.sum(lss.coef_ != 0))

print('最小2乗誤差 : ', mean_squared_error(y_test,y_pred))


result_1600 = []
result_1700 = []
result_1800 = []
for i in range(len(y_test)):
    if y_test[i] == 1600:
        result_1600.append(y_pred[i])
    elif y_test[i] == 1700:
        result_1700.append(y_pred[i])
    elif y_test[i] == 1800:
        result_1800.append(y_pred[i])

print('1600の平均値 : ', sum(result_1600)/len(result_1600))
print('1700の平均値 : ', sum(result_1700)/len(result_1700))
print('1800の平均値 : ', sum(result_1800)/len(result_1800))


plt.scatter(y_pred, y_test)
plt.xlabel("predict")
plt.ylabel("true")
plt.savefig("learning_reg_" + str(phase) + str(dimension) + ".png")
# plt.show()