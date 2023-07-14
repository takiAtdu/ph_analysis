import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc

from skimage.filters import threshold_multiotsu

# 画像の読み込み
print("画像を読み込み中です。")
input_image = "r1_500x_1.png"
input_image_path = "data/" + input_image
image_path = os.path.splitext(input_image)[0]
output_path = "output/" + image_path

# mode="L" とするとグレースケールで読み込まれる
pict = imageio.v3.imread(input_image_path, mode="L")


# 閾値の設定
print("閾値を設定中です。")
# from scipy.signal import argrelmin, argrelmax

# データの生成
histo, bins = np.histogram(pict.ravel(), range=(0,256), bins=256)
x=bins[1:]
y=histo

# 極値の取得
# orderを変えることで調整可能
order = 14
arg_r_min,arg_r_max=argrelmin(y, order=order),argrelmax(y, order=order)

# 極小値のリストから、適切な値のみ抽出
arg_r_min_picked = [i for i in arg_r_min[0] if (20 < i) & (i < 180)]

# 極値を自分で設定する場合
#arg_r_min_picked = [50, 140]

# 大津の方法
thresholds = threshold_multiotsu(pict)
print(thresholds)
print(thresholds[0])
print(thresholds[1])


# 抽出した極小値を表示

# figureとaxesを同時生成
fig, ax = plt.subplots()
# 第3引数はcolor cycle
ax.plot(x,y,"C2")
# 第2引数"ro"は、赤い点で表示の意味
ax.plot(x[arg_r_min_picked],y[arg_r_min_picked],"ro",label="argrelmin")
# 凡例
plt.legend()
# 軸ラベルを追加
ax.set(ylabel="Frequency")
# 保存
plt.savefig(output_path+"-arg_rel_minmax.png")
print("極小値をプロットしたヒストグラムを保存しました。")