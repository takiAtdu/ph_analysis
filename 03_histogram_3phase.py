import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import glob

from skimage.filters import threshold_multiotsu

import common

condition = input("熱処理条件_倍率(data内から選択) : ")
filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data/" + condition + "/*.png")
filenames.sort()

for png_path in filenames:
  # 画像名（拡張子を抜いたもの）（ex: sample.png -> sample）
  image_name = os.path.splitext(os.path.basename(png_path))[0]

  pict = common.read_image(png_path)



  # 大津の多値化
  thresholds = common.get_thresholds(pict)


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
  # 軸の設定
  plt.rcParams['xtick.direction'] = 'in'
  plt.rcParams['ytick.direction'] = 'in'
  plt.yscale('log')
  ax.set(ylabel="Frequency")
  # 保存
  plt.savefig("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/histo/" + image_name + "-histo.png")