import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import glob

from skimage.filters import threshold_multiotsu

filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data/AsCast_500x" + "/*.png")
filenames.sort()

for png_path in filenames:
  # 画像の読み込み
  image_name = os.path.splitext(os.path.basename(png_path))[0]
  
  # #画像名（拡張子を抜いたもの）（ex: sample.png -> sample）
  # image_path = os.path.splitext(input_image)[0]
  # # 出力先のパス
  # output_path = image_path
  # mode="L" とするとグレースケールで読み込まれる
  pict = imageio.v3.imread(png_path, mode="L")



  # 大津の多値化
  thresholds = threshold_multiotsu(pict)
  print(thresholds)



  # 抽出した極小値を表示

  # データの生成
  histo, bins = np.histogram(pict.ravel(), range=(0,256), bins=256)
  x=bins[1:]
  y=histo
  # figureとaxesを同時生成
  fig, ax = plt.subplots()
  # 第3引数はcolor cycle
  ax.plot(x, y, "C2", linewidth=5)
  # 第2引数"ro"は、赤い点で表示の意味
  ax.plot(x[thresholds],y[thresholds],"ro",label="argrelmin")
  # 凡例
  plt.legend()
  # 軸ラベルを追加
  ax.set(ylabel="Frequency")
  # 保存
  plt.savefig("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/histo/" + image_name + "-histo.png")