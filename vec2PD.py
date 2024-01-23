import matplotlib.pyplot as plt
import homcloud.interface as hc

phase = "moss"
dimension = 1
pd_range = (-40, 40)
sigma = 1
weight = ("atan", 0.01, 2)

diagonal = []
for i in range(64):
    if i == 0:
        diagonal.append(i)
    else:
        x = diagonal[i-1] + i + 1
        diagonal.append(x)


pdname = "/Users/takigawaatsushi/Documents/研究室/研究/ph_analysis/for_vec/pdgm_moss/1600c3h_500x_002-pd_moss.pdgm"
print(pdname)

# PH解析の結果を取得
pd = hc.PDList(pdname).dth_diagram(dimension)

# ベクトル化
spec = hc.PIVectorizeSpec(pd_range, 64, sigma = sigma, weight = weight)
pdvect = spec.vectorize(pd)

print(pdvect.shape)

for i in diagonal:
    pdvect[i] = 0
    pdvect[i-1] = 0

spec.histogram_from_vector(pdvect).plot(colorbar={"type": "linear"})

# 出力
plt.savefig("vec2PD_" + phase + str(dimension) + ".png")