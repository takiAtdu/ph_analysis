import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

from skimage.filters import threshold_otsu


# 画像の読み込み
input_image = "ioroi_sample.png"
# 入力画像のパス
input_image_path = "data/" + input_image
#画像名（拡張子を抜いたもの）（ex: sample.png -> sample）
image_path = os.path.splitext(input_image)[0]
# 出力先のパス
output_path = "data/" + image_path
# mode="L" とするとグレースケールで読み込まれる
pict = imageio.v3.imread(input_image_path, mode="L")



# 大津の2値化
thresholds = threshold_otsu(pict)
print(thresholds)



# 抽出した極小値を表示

# データの生成
histo, bins = np.histogram(pict.ravel(), range=(0,256), bins=256)
x=bins[1:]
y=histo
# figureとaxesを同時生成
fig, ax = plt.subplots()
# 第3引数はcolor cycle
ax.plot(x,y,"C2")
# 第2引数"ro"は、赤い点で表示の意味
ax.plot(x[thresholds],y[thresholds],"ro",label="argrelmin")
# 凡例
plt.legend()
# 軸ラベルを追加
ax.set(ylabel="Frequency")
# 保存
plt.savefig(output_path+"-histogram-2phase.png")