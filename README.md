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
3. binary_image.pyで2値化画像を確認
4. histogram_3phase.pyでヒスグラムを確認
5. phanalysis.pyでph解析を実行
6. PD.pyでPDを表示
1. vectorize.pyでベクトル化
7. classification.pyで分類
8. lasso.pyで機械学習
9. coef_cmap.pyで係数確認
11. reverse/に逆解析したい画像を追加
12. reverse.pyで逆解析