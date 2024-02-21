# https://helve-blog.com/posts/python/sklearn-lasso-regression/

import homcloud.interface as hc
import glob
import pickle
import os

import imageio
from skimage.filters import threshold_multiotsu

import common

# moss, t2, tic
phase = input("相(moss, t2, tic) : ")
# 1, 0
dimension = int(input("次元(0, 1) : "))

# ascast, 1600c3h
condition = input("熱処理条件(AsCast, 1600c3h, ..) : ")
images = glob.glob("reverse/data/"+condition+"/*.png")
images.sort()

x_min = float(input("逆解析範囲のx_min : "))
x_max = x_min + 1.25
y_min = float(input("逆解析範囲のy_min : "))
y_max = y_min + 1.25

print("ph解析開始")

for png_path in images:
    print(png_path)
    image_name = os.path.splitext(os.path.basename(png_path))[0]

    pict = common.read_image(png_path)

    # 2値化
    # 大津の方法
    thresholds = common.get_thresholds(pict)

    os.makedirs("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/reverse/output/"+condition+"/"+str(phase)+str(dimension), exist_ok=True)
    save_to="/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/reverse/output/"+condition+"/"+str(phase)+str(dimension)+"/"+image_name+"_phtrees.pdgm"
    is_file = os.path.isfile(save_to)


    if phase == "tic":
        pict_tic = pict > thresholds[0]
        if not is_file:
            pd = hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_tic, signed=True), save_to=save_to)
    if phase == "t2":
        pict_t2 = (thresholds[0] >= pict) | (pict >= thresholds[1])
        if not is_file:
            pd = hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_t2, signed=True), save_to=save_to)
    if phase == "moss":
        pict_moss = thresholds[1] > pict
        if not is_file:
            pd = hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_moss, signed=True), save_to=save_to)

print("ph解析終了")


print("逆解析開始")
pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/reverse/output/"+condition+"/"+str(phase)+str(dimension)+"/*.pdgm")
pdnames.sort()


# PH解析の結果を取得
phtrees_list = [hc.PDList(pdname).bitmap_phtrees(dimension) for pdname in pdnames]
nodes_list = [phtrees.pair_nodes_in_rectangle(x_min, y_min, x_max, y_max) for phtrees in phtrees_list]

for i, image in enumerate(images):
    image_name = os.path.splitext(os.path.basename(image))[0]
    nodes = nodes_list[i]
    # # 10点取り出す
    # print("len(nodes_list[i]) : ", str(len(nodes_list[i])))
    # if len(nodes_list[i]) > 100:
    #     nodes = nodes_list[i][2000:2002]
    #     # print("len(nodes) : ", str(len(nodes)))
    #     print("nodes : ", nodes)
    # else:
    #     nodes = nodes_list[i]
    #     print("len(nodes) : ", str(len(nodes)))
    #     print("nodes : ", nodes)
    reverse = hc.draw_volumes_on_2d_image(nodes, image, color=(255, 0, 0), alpha=0.5, birth_position=(0, 255, 0))

    save_to = "reverse/output/"+condition+"/"+phase+str(dimension)+"/"+image_name+"_reverse_"+str(x_min)+"_"+str(y_min)+".png"
    reverse.save(save_to)
    print(save_to)