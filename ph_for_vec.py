# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import imageio
import os
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu
import glob
import numpy as np


filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data/1800_3h_500x" + "/*.png")
filenames.sort()


for png_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    image_name = os.path.splitext(os.path.basename(png_path))[0]
    print(png_path)

    # mode="L" とするとグレースケールで読み込まれる
    pict = imageio.v3.imread(png_path, mode="L")


    # 閾値の設定
    print("閾値を設定中です。")
    # 大津の方法
    arg_r_min_picked = threshold_multiotsu(pict)


    # PH解析
    print("PH解析中です。")

    # 2値化
    pict_tic = pict > arg_r_min_picked[0]
    pict_t2 = (arg_r_min_picked[0] >= pict) | (pict >= arg_r_min_picked[1])
    pict_moss = arg_r_min_picked[1] > pict

    tic_count = np.count_nonzero(pict < arg_r_min_picked[0])
    t2_count = np.count_nonzero((arg_r_min_picked[0] <= pict) & (pict <= arg_r_min_picked[1]))
    moss_count = np.count_nonzero(arg_r_min_picked[1] < pict)

    sum = tic_count + t2_count + moss_count

    print("-----相分率-----")
    print("TiC : ", tic_count/sum*100)
    print("T2 : ", t2_count/sum*100)
    print("Moss : ", moss_count/sum*100)

    # 白黒画像の表示
    # plt.imshow(pict_tic, "gray")
    # plt.savefig(output_path+"-binary_tic.png")

    # plt.imshow(pict_t2, "gray")
    # plt.savefig(output_path+"-binary_t2.png")

    # plt.imshow(pict_moss, "gray")
    # plt.savefig(output_path+"-binary_moss.png")

    # PH解析
    pd_result_path = "output/"
    os.makedirs(pd_result_path+"pdgm_tic/", exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_tic, signed=True), save_to=pd_result_path+"pdgm_tic/"+image_name+"-pd_tic.pdgm")
    os.makedirs(pd_result_path+"pdgm_t2/", exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_t2, signed=True), save_to=pd_result_path+"pdgm_t2/"+image_name+"-pd_t2.pdgm")
    os.makedirs(pd_result_path+"pdgm_moss/", exist_ok=True)
    hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_moss, signed=True), save_to=pd_result_path+"pdgm_moss/"+image_name+"-pd_moss.pdgm")

    print(pd_result_path+"pdgm_tic/"+image_name+"-pd_tic.pdgm")
    print(pd_result_path+"pdgm_t2/"+image_name+"-pd_t2.pdgm")
    print(pd_result_path+"pdgm_moss/"+image_name+"-pd_moss.pdgm")