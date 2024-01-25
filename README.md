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
2. dataにpng画像を保存
3. binary_image.pyで2値化画像を確認
4. histogram_3phase.pyでヒスグラムを確認
5. ph_for_vec.pyでph解析を実行
6. pd_image.pyでPDを表示
7. for_vecにpdgmファイルを入れ、classification.pyでベクトル化、分類
8. learning_reg.pyで機械学習
9. coef_cmap.pyで係数確認
10. pca2PD.pyで主成分が示す領域を確認
11. for_reverseに逆解析したい画像を追加
12. reverse.pyで逆解析