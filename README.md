# 概要
Intel Macでのパーシステントホモロジー解析
[参考]("https://homcloud.dev/install-guide/install_guide_for_Mac.html")

# homebrewでパッケージをインストール
```
$ brew install cgal cmake open-mpi qt
```

# 仮想環境
```
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv)$
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