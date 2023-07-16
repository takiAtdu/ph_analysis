import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu
import glob
from sklearn.decomposition import PCA


filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data_for_vec/*.png")

pd_result_path = "output_for_vec/ph_results/"
os.makedirs(pd_result_path, exist_ok=True)
i = 0
for png_path in filenames:
    i += 1
    print("===No."+str(i)+"===")
    # 画像の読み込み
    print("画像を読み込み中です。")
    input_image = os.path.basename(png_path)
    input_image_path = "data_for_vec/" + input_image
    image_path = os.path.splitext(input_image)[0]
    output_path = "output_for_vec/" + image_path

    # mode="L" とするとグレースケールで読み込まれる
    pict = imageio.v3.imread(input_image_path, mode="L")

    # 閾値の設定
    print("閾値を設定中です。")
    # from scipy.signal import argrelmin, argrelmax

    # データの生成
    histo, bins = np.histogram(pict.ravel(), range=(0,256), bins=256)
    x=bins[1:]
    y=histo

    # 大津の方法
    arg_r_min_picked = threshold_multiotsu(pict)

    # PH解析
    print("PH解析中です。")

    # 2値化
    pict_tic = pict > arg_r_min_picked[0]
    pict_t2 = (arg_r_min_picked[0] >= pict) | (pict >= arg_r_min_picked[1])
    pict_moss = arg_r_min_picked[1] > pict

    # PH解析
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_tic, signed=True), save_to=pd_result_path+image_path+"-pd_tic.pdgm")
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_t2, signed=True), save_to=pd_result_path+image_path+"-pd_t2.pdgm")
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_moss, signed=True), save_to=pd_result_path+image_path+"-pd_moss.pdgm")