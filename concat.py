import cv2
import glob
import numpy as np

filenames = glob.glob('/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output/binaryimage_tic/1600d1d_500x' + '/*.png')
filenames.sort()

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def add_blank(img):
    #同じ高さのブランク画像を生成
    height = img.shape[0]
    width = img.shape[1]
    blank_h = np.zeros((height, 5, 3), np.uint8)
    blank_v = np.zeros((5, width+10, 3), np.uint8)
    #0配列は黒なので全要素を255にする
    blank_h += 255
    blank_v += 255
    #画像とブランクを連結
    img = cv2.hconcat([blank_h, img, blank_h])
    img = cv2.vconcat([blank_v, img, blank_v])

    return img

im1_s = []
for filename in filenames:
    print(filename)
    
    img = cv2.imread(filename)
    # img = add_blank(img)
    im1_s.append(img)

im_tile = concat_tile([[im1_s[0], im1_s[1], im1_s[2], im1_s[3], im1_s[4]],
                        [im1_s[5], im1_s[6], im1_s[7], im1_s[8], im1_s[9]],
                        [im1_s[10], im1_s[11], im1_s[12], im1_s[13], im1_s[14]],
                        [im1_s[15], im1_s[16], im1_s[17], im1_s[18], im1_s[19]],])
cv2.imwrite('concat.png', im_tile)