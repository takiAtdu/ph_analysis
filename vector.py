import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from scipy.signal import argrelmin, argrelmax
import homcloud.interface as hc
from skimage.filters import threshold_multiotsu
import glob
from sklearn.decomposition import PCA

labels = np.array(
        [
        1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 
        1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 
        2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 
        2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 
        ]
        )


pdnames = glob.glob("/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/output_for_vec/ph_results/*.pdgm")
pdnames.sort()
# for pdname in pdnames:
#     print(pdname)

dimension = 1
pds = [hc.PDList(pdname).dth_diagram(dimension) for pdname in pdnames]

spec = hc.PIVectorizeSpec((-40, 40), 128, sigma=0.001, weight=("atan", 0.1, 10))
pdvects = np.vstack([spec.vectorize(pd) for pd in pds])
pdvects = pdvects / pdvects.max()


pca = PCA(n_components=2)
pca.fit(pdvects)

reduced = pca.transform(pdvects)

plt.gca().set_aspect('equal')  # Set the aspect ratio of the figure
plt.scatter(reduced[labels == 1, 0], reduced[labels == 1, 1], c="r")  # Show 1-labled data by "r"ed
plt.scatter(reduced[labels == 2, 0], reduced[labels == 2, 1], c="b")  # Show 2-labled data by "b"lue
#plt.scatter(reduced[labels == 3, 0], reduced[labels == 3, 1], c="g")  # Show 3-labled data by "b"lue


plt.savefig("result.png")