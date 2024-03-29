import os
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
import homcloud.interface as hc

import common

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
sigma = common.sigma
weight = common.weight
bins = common.bins
pd_range = common.pd_range
diagonal = common.diagonal


X = []
Y = []
for i in range(bins):
    x    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*i
    y = x
    x_dx = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(i+1)
    y_dy = x_dx

    X.append((x+x_dx)/2)
    Y.append((y+y_dy)/2)


print("係数取得開始")

model = "output/lasso/lasso_"+ phase + str(dimension) + ".sav"
lss = pickle.load(open(model, 'rb'))
coef = lss.coef_

count = 0
effective_coef_dict = {}
effective_coef_list = []
for i in range(bins):
    for j in range(i+1):
        count += 1
        if lss.coef_[count-1] != 0:
            # print(count, "は", i+1, "行目, ", j+1, "列目で、値は", lss.coef_[count-1])

            x    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*j
            y    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*i
            x_dx = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(j+1)
            y_dy = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(i+1)

            effective_coef_dict[(x, y, x_dx, y_dy)] = lss.coef_[count-1]
            effective_coef_list.append([x, y, x_dx, y_dy, lss.coef_[count-1]])

# effective_coef_list = sorted(effective_coef_dict.items(), key = lambda coef : abs(coef[1]), reverse=True)
# effective_coef_list = sorted(effective_coef_dict.items(), key = lambda coef : coef[1], reverse=True)
# print(effective_coef_list)



print("係数取得終了")


print("描画開始")

spec = hc.PIVectorizeSpec(pd_range, bins, sigma = sigma, weight = "none")
spec.histogram_from_vector(coef).plot(colorbar={"type": "linear-midpoint", "midpoint": 0})

save_dir = "output/coefmap/"
os.makedirs(save_dir, exist_ok=True)
save_path = save_dir + "coefmap_" + phase + str(dimension)
plt.savefig(save_path + ".png")

effective_coef_array = np.array(effective_coef_list)
df_effective_coef = pd.DataFrame(data=effective_coef_array, columns=["x", "y", "x_dx", "y_dy", "coef"])
df_effective_coef = df_effective_coef.sort_values("coef", ascending=False)
print(df_effective_coef)
effective_coef_array = df_effective_coef.to_numpy()
np.save(save_path + ".npy", effective_coef_array)