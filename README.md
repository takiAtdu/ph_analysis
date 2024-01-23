# 概要
Intel Macでのパーシステントホモロジー解析
[参考]("https://homcloud.dev/install-guide/install_guide_for_Mac.html")

# homebrewでパッケージをインストール
```
$ brew install cgal cmake open-mpi qt
```

# 仮想環境
```
$ python -m venv venv
$ source ./venv/bin/activate
(venv)$
```

# 仮想環境のパッケージを出力
```
(venv)$ pip freeze > requirements.txt
```

# 仮想環境にパッケージをインストール
```
(venv)$ pip install -r requirements.txt
```

# 入出力ディレクトリを作成
```
(venv)$ mkdir data
(venv)$ mkdir output
```

# 実行手順
1. bmp_to_png.pyでpng画像を生成
2. binary_image.pyで2値化画像を確認
3. histogram_3phase.pyでヒスグラムを確認
4. ph_for_vec.pyでph解析を実行
5. pd_image.pyでPDを表示
6. for_vecにpdgmファイルを入れ、classification.pyでベクトル化、分類
7. learning_reg.pyで機械学習
8. coef_cmap.pyで係数確認
9. pca2PD.pyで主成分が示す領域を確認
10. reverse.pyで逆解析