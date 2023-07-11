import os
from PIL import Image
import glob

filenames = glob.glob("data/*.bmp")

for bmpname in filenames:
	image = Image.open(bmpname)
	pngname = os.path.splitext(bmpname)[0] + ".png"
	image.save(pngname)