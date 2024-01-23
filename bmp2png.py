import os
from PIL import Image
import glob
import cv2

basedir = "/Users/takigawaatsushi/Documents/研究室/研究/data/EPMA/240119/ascast_500x"
filepaths = glob.glob(basedir + "/*.bmp")
filepaths.sort()
savedir = basedir + "/png/"
os.makedirs(savedir, exist_ok=True)

for bmppath in filepaths:
	print("-------------------------")
	print(bmppath)
	image = Image.open(bmppath)
	pngname = os.path.splitext(os.path.basename(bmppath))[0] + ".png"
	print(pngname)
	pngpath = savedir + pngname
	print(pngpath)
	image.save(pngpath)

	# 画像読み込み
	img = cv2.imread(pngpath)

	# img[top : bottom, left : right]
	cut_img = img[0 : 960, 0: 1280]
	cv2.imwrite(pngpath, cut_img)