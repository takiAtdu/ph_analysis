# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu
import glob


filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/data/*.png")


for input_image in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    #input_image = "r1_1000x_1.png"
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

    # # 極値の取得
    # # orderを変えることで調整可能
    # order = 14
    # arg_r_min,arg_r_max=argrelmin(y, order=order),argrelmax(y, order=order)

    # # 極小値のリストから、適切な値のみ抽出
    # arg_r_min_picked = [i for i in arg_r_min[0] if (20 < i) & (i < 180)]

    # # 極値を自分で設定する場合
    # #arg_r_min_picked = [50, 140]

    # 大津の方法
    arg_r_min_picked = threshold_multiotsu(pict)


    # # 抽出した極小値を表示

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
    os.makedirs("output/min/", exist_ok=True)
    plt.savefig("output/min/"+image_path+"-arg_rel_minmax.png")
    print("極小値をプロットしたヒストグラムを保存しました。")


    # PH解析
    print("PH解析中です。")
    # homcloudのインポート
    # import homcloud.interface as hc

    # 2値化
    pict_tic = pict > arg_r_min_picked[0]
    pict_t2_mo2c = (arg_r_min_picked[0] >= pict) | (pict >= arg_r_min_picked[1])
    pict_moss = arg_r_min_picked[1] > pict

    # plt.imshow(pict_tic, "gray")
    # plt.savefig(output_path+"-binary_tic.png")

    # plt.imshow(pict_t2_mo2c, "gray")
    # plt.savefig(output_path+"-binary_t2_mo2c.png")

    # plt.imshow(pict_moss, "gray")
    # plt.savefig(output_path+"-binary_moss.png")

    # PH解析
    # hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_tic, signed=True), save_to=output_path+"-pd_tic.pdgm")
    # hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_t2_mo2c, signed=True), save_to=output_path+"-pd_t2_mo2c.pdgm")
    # hc.PDList.from_bitmap_levelset(hc.distance_transform(pict_moss, signed=True), save_to=output_path+"-pd_moss.pdgm")

    # PH図を取得
    dimension = 1
    pd_tic = hc.PDList(output_path+"-pd_tic.pdgm").dth_diagram(dimension)
    pd_t2_mo2c = hc.PDList(output_path+"-pd_t2_mo2c.pdgm").dth_diagram(dimension)
    pd_moss = hc.PDList(output_path+"-pd_moss.pdgm").dth_diagram(dimension)

    # PH図を表示
    os.makedirs("output/pd/", exist_ok=True)
    pd_tic.histogram(x_bins=64).plot(colorbar={"type": "log"})
    plt.savefig("output/pd/"+image_path+"-pdimage_tic.png")
    pd_t2_mo2c.histogram(x_bins=64).plot(colorbar={"type": "log"})
    plt.savefig("output/pd/"+image_path+"-pdimage_t2_mo2c.png")
    pd_moss.histogram(x_bins=64).plot(colorbar={"type": "log"})
    plt.savefig("output/pd/"+image_path+"-pdimage_moss.png")
    print(str(dimension)+"次のPH図を保存しました。")