# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import matplotlib.pyplot as plt
import os
import homcloud.interface as hc
import glob

import common

phase = input("phase(moss, t2, tic) : ")
dimension = int(input("dimension(0, 1) : "))
pd_range = common.pd_range
bins = common.bins

condition = input("熱処理条件 : ")
filenames = glob.glob("output/pdgm_" + phase + "/" + condition + "*.pdgm")
filenames.sort()


for pdgm_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    print(pdgm_path)
    pdgm_name = os.path.splitext(os.path.basename(pdgm_path))[0]

    save_dir = "output/pd" + str(dimension) + "_" + phase + "/" + condition + "/"
    save_filename = pdgm_name +".png"
    print(save_dir + save_filename)

    # PDを取得
    pd_result_path = "output/ph_results/"
    pd = hc.PDList(pdgm_path).dth_diagram(dimension)

    # PDを保存
    os.makedirs(save_dir, exist_ok=True)
    pd.histogram(x_range=(pd_range[0]-0.5, pd_range[1]+0.5), x_bins=bins).plot(colorbar={"type": "log"})
    plt.savefig(save_dir + save_filename)

    print(str(dimension)+"次のPH図を保存しました。")

    plt.clf()
    plt.close()