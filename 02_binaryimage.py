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

    pict = common.read_image(png_path)

    # 閾値の設定
    print("閾値を設定中です。")
    thresholds = common.get_thresholds(pict)

    # PH解析
    print("PH解析中です。")
    # 2値化
    pict_tic, pict_t2, pict_moss = common.binarize(pict, thresholds)

    tic_count = np.count_nonzero(pict_tic)
    t2_count = np.count_nonzero(pict_t2)
    moss_count = np.count_nonzero(pict_moss)

    sum = tic_count + t2_count + moss_count

    tic_rate_sum += tic_count/sum*100
    t2_rate_sum += t2_count/sum*100
    moss_rate_sum += moss_count/sum*100

    # 対象相が1になっているので、反転
    pict_tic = np.logical_not(pict_tic)
    pict_t2 = np.logical_not(pict_t2)
    pict_moss = np.logical_not(pict_moss)

    # 白黒画像の表示
    os.makedirs("output/binaryimage_tic/" + condition + "/", exist_ok=True)
    os.makedirs("output/binaryimage_t2/" + condition + "/", exist_ok=True)
    os.makedirs("output/binaryimage_moss/" + condition + "/", exist_ok=True)
    Image.fromarray(pict_tic).save("output/binaryimage_tic/" + condition + "/" + image_name + "-binary_tic.png")
    Image.fromarray(pict_t2).save("output/binaryimage_t2/" + condition + "/" + image_name + "-binary_t2.png")
    Image.fromarray(pict_moss).save("output/binaryimage_moss/" + condition + "/" + image_name + "-binary_moss.png")

len = len(filenames)
print("-----相分率-----")
print("TiC : ", tic_rate_sum/len)
print("T2 : ", t2_rate_sum/len)
print("Moss : ", moss_rate_sum/len)