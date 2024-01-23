# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import matplotlib.pyplot as plt
import imageio
import os
from skimage.filters import threshold_multiotsu
import glob
import numpy as np
from PIL import Image


filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data/AsCast_500x" + "/*.png")
filenames.sort()

tic_rate_sum = 0
t2_rate_sum = 0
moss_rate_sum = 0

for png_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    image_name = os.path.splitext(os.path.basename(png_path))[0]
    print(png_path)
    print(image_name)

    # mode="L" とするとグレースケールで読み込まれる
    pict = imageio.v3.imread(png_path, mode="L")


    # 閾値の設定
    print("閾値を設定中です。")
    # 大津の方法
    arg_r_min_picked = threshold_multiotsu(pict)


    # PH解析
    print("2値化中です。")

    # 2値化
    pict_tic = (pict > arg_r_min_picked[0]) * 255
    pict_t2 = ((arg_r_min_picked[0] >= pict) | (pict >= arg_r_min_picked[1])) * 255
    pict_moss = (arg_r_min_picked[1] > pict) * 255

    tic_count = np.count_nonzero(pict < arg_r_min_picked[0])
    t2_count = np.count_nonzero((arg_r_min_picked[0] <= pict) & (pict <= arg_r_min_picked[1]))
    moss_count = np.count_nonzero(arg_r_min_picked[1] < pict)

    sum = tic_count + t2_count + moss_count

    # print("-----相分率-----")
    # print("TiC : ", tic_count/sum*100)
    # print("T2 : ", t2_count/sum*100)
    # print("Moss : ", moss_count/sum*100)

    tic_rate_sum += tic_count/sum*100
    t2_rate_sum += t2_count/sum*100
    moss_rate_sum += moss_count/sum*100

    # 白黒画像の表示
    Image.fromarray(np.uint8(pict_tic)).save("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/binaryimage_tic/" + image_name + "-binary_tic.png")
    Image.fromarray(np.uint8(pict_t2)).save("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/binaryimage_t2/" + image_name + "-binary_t2.png")
    Image.fromarray(np.uint8(pict_moss)).save("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/binaryimage_moss/" + image_name + "-binary_moss.png")

len = len(filenames)
print("-----相分率-----")
print("TiC : ", tic_rate_sum/len)
print("T2 : ", t2_rate_sum/len)
print("Moss : ", moss_rate_sum/len)