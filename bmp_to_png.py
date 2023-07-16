import os
from PIL import Image
import glob
import cv2

filenames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/data/EPMA/230714/*.bmp")

for bmpname in filenames:
	image = Image.open(bmpname)
	pngname = os.path.splitext(bmpname)[0] + ".png"
	image.save(pngname)

	# 画像読み込み
	img = cv2.imread(pngname)

	# img[top : bottom, left : right]
	cut_img = img[0 : 960, 0: 1280]
	cv2.imwrite(pngname, cut_img)