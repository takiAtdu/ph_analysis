# https://homcloud.dev/python-api/interface.html#homcloud.interface.draw_volumes_on_2d_image

import matplotlib.pyplot as plt
import os
import homcloud.interface as hc
import glob

phase = "moss"
dimension = 1

filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/pdgm_" + phase + "/*.pdgm")
filenames.sort()


for pdgm_path in filenames:
    # 画像の読み込み
    print("画像を読み込み中です。")
    pdgm_name = os.path.splitext(os.path.basename(pdgm_path))[0]
    print(pdgm_path)
    save_dir = "output/pd" + str(dimension) + "_" + phase + "/"
    save_filename = pdgm_name +".png"
    print(save_dir + save_filename)

    # PDを取得
    pd_result_path = "output/ph_results/"
    pd_moss = hc.PDList(pdgm_path).dth_diagram(dimension)

    # PDを表示
    os.makedirs(save_dir, exist_ok=True)
    pd_moss.histogram(x_range=(-40.5, 40.5), x_bins=64).plot(colorbar={"type": "log"})
    plt.savefig(save_dir + save_filename)

    print(str(dimension)+"次のPH図を保存しました。")

    plt.clf()
    plt.close()