# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import matplotlib.pyplot as plt
import imageio
import os
from skimage.filters import threshold_multiotsu
import glob
import numpy as np
from PIL import Image

import common

condition = input("熱処理条件_倍率(data内から選択) : ")
filenames = glob.glob("data/" + condition + "/*.png")
filenames.sort()

tic_rate_sum = 0
t2_rate_sum = 0
moss_rate_sum = 0

for png_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    print(png_path)
    image_name = os.path.splitext(os.path.basename(png_path))[0]

    # mode="L" とするとグレースケールで読み込まれる
    pict = common.read_image(png_path)

    # 閾値の設定
    print("閾値を設定中です。")
    thresholds = common.get_thresholds(pict)

    # PH解析
    print("PH解析中です。")
    # 2値化
    pict_tic, pict_t2, pict_moss = common.binarize(pict, thresholds)
    pict_tic *= 255
    pict_t2 *= 255
    pict_moss *= 255

    tic_count = np.count_nonzero(pict < thresholds[0])
    t2_count = np.count_nonzero((thresholds[0] <= pict) & (pict <= thresholds[1]))
    moss_count = np.count_nonzero(thresholds[1] < pict)

    sum = tic_count + t2_count + moss_count

    tic_rate_sum += tic_count/sum*100
    t2_rate_sum += t2_count/sum*100
    moss_rate_sum += moss_count/sum*100

    # 白黒画像の表示
    Image.fromarray(np.uint8(pict_tic)).save("output/binaryimage_tic/" + condition + "/" + image_name + "-binary_tic.png")
    Image.fromarray(np.uint8(pict_t2)).save("output/binaryimage_t2/" + condition + "/" + image_name + "-binary_t2.png")
    Image.fromarray(np.uint8(pict_moss)).save("output/binaryimage_moss/" + condition + "/" + image_name + "-binary_moss.png")

len = len(filenames)
print("-----相分率-----")
print("TiC : ", tic_rate_sum/len)
print("T2 : ", t2_rate_sum/len)
print("Moss : ", moss_rate_sum/len)