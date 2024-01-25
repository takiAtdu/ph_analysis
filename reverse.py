# https://helve-blog.com/posts/python/sklearn-lasso-regression/

import homcloud.interface as hc
import glob
import pickle
import os

import imageio
from skimage.filters import threshold_multiotsu


phase = "moss"
dimension = 1
pd_range = (-40, 40)
bins = 64
sigma = 1
weight = ("atan", 0.01, 10)

condition = "1800_3h_500x"
images = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/for_reverse/"+condition+"/images/*.png")
images.sort()

print("ph解析開始")

pdnames = []
for png_path in images:
    print(png_path)

    pict = imageio.v3.imread(png_path, mode="L")

    # 大津の方法
    arg_r_min_picked = threshold_multiotsu(pict)

    # 2値化
    # pict_tic = pict > arg_r_min_picked[0]
    # pict_t2 = (arg_r_min_picked[0] >= pict) | (pict >= arg_r_min_picked[1])
    pict_moss = arg_r_min_picked[1] > pict

    # hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_tic, signed=True))
    # hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_t2, signed=True))
    pd = hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(pict_moss, signed=True))
    pdnames.append(pd)

# print("ph解析終了")


# print("係数取得開始")

# model = 'model_reg.sav'
# lss = pickle.load(open(model, 'rb'))

# count = 0
# effective_coef_dict = {}
# for i in range(64):
#     for j in range(i+1):
#         count += 1
#         if lss.coef_[count-1] != 0:
#             # print(count, "は", i+1, "行目, ", j+1, "列目で、値は", lss.coef_[count-1])

#             x    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*j
#             y    = pd_range[0]+(pd_range[1]-pd_range[0])/bins*i
#             x_dx = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(j+1)
#             y_dy = pd_range[0]+(pd_range[1]-pd_range[0])/bins*(i+1)

#             effective_coef_dict[(x, y, x_dx, y_dy)] = lss.coef_[count-1]

# effective_coef_list = sorted(effective_coef_dict.items(), key = lambda coef : abs(coef[1]), reverse=True)
# print(effective_coef_list)

# print("係数取得終了")

print("逆解析開始")

# PH解析の結果を取得
phtrees_list = [pdname.bitmap_phtrees(dimension) for pdname in pdnames]
nodes_list = [phtrees.pair_nodes_in_rectangle(-1.25, 12.5, 0.0, 13.75) for phtrees in phtrees_list]

for i, image in enumerate(images):
    image_name = os.path.splitext(os.path.basename(image))[0]
    nodes = nodes_list[i]
    reverse = hc.draw_volumes_on_2d_image(nodes, image, color=(255, 0, 0), alpha=0.5, birth_position=(0, 255, 0))

    reverse.save("for_reverse/output/"+condition+"/"+phase+"/"+image_name+"_reverse.png")
    print("for_reverse/output/"+condition+"/"+phase+"/"+image_name+"_reverse.png")