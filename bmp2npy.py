import os
from PIL import Image
import glob
import cv2
import numpy as np
import common


condition = input("熱処理条件_倍率(data内から選択) : ")
basedir = input("パスを指定(ex. /Users/takigawaatsushi/Documents/研究室/研究/data/EPMA/240205/1800c24h) : ")
filepaths = glob.glob(basedir + "/*.bmp")
filepaths.sort()
savedir = "data/npy/"
os.makedirs(savedir, exist_ok=True)

data_list = []
for filepath in filepaths:
	print("-------------------------")
	print(filepath)

	# 画像読み込み
	img = common.read_image(filepath)
	print(img.shape)
	
	cut_img = img[0 : 960, 0: 1280]
	print(cut_img.shape)
	
	data_list.append(cut_img)

imgs = np.array(data_list)
np.save(savedir + condition + ".npy", imgs)