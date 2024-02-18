from skimage.filters import threshold_multiotsu
import imageio

pd_range = (-40, 40)
bins = 64
sigma = 1
weight = ("atan", 0.01, 10)


diagonal = []
for i in range(64):
    if i == 0:
        diagonal.append(i)
    else:
        x = diagonal[i-1] + i + 1
        diagonal.append(x)


def get_thresholds(pict):
    # 大津の方法
    thresholds = threshold_multiotsu(pict)
    thresholds[1] += 20
    return thresholds

def read_image(png_path):
  pict = imageio.v3.imread(png_path, mode="L")
  return pict

def binarize(pict, thresholds):
  pict_tic = pict > thresholds[0]
  pict_t2 = (thresholds[0] >= pict) | (pict >= thresholds[1])
  pict_moss = (thresholds[1]) > pict

  return pict_tic, pict_t2, pict_moss

def get_hv():
  hv = [952.4, 925.2, 955.9, 850.2, 948.1, 983.4]
  return hv