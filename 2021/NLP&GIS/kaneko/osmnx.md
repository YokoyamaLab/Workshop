# OSMnx
OpenStreetMapからストリートネットワークを取得、構築、分析、視覚化するPythonのライブラリ

## メリット
- 運転しやすい、自転車に乗りやすい、歩きやすい道のネットワークをダウンロードし、解析、可視化することができる
- 1行のコードで世界中のストリートネットワークをダウンロードできる
- ネットワークに沿った出発地と目的地のルートを計算し、それらを素早く視覚化することができる

## デメリット
OpenStreetMap (OSM) のAPIを利用しており、OSMは誰でも自由に編集することが可能であるため、正確さが懸念される

## 使用例
- 対象の地域の道路の可視化
- 2点間の最短経路の検索、可視化
- 道路の向きがどれくらいの頻度で登場するのかを図示することで都市の複雑さを比較する

## 例
```
# https://sinyblog.com/python/osmnx-001/
import networkx as nx
import osmnx as ox
import requests
import sys,os,os.path
import matplotlib.cm as cm
import matplotlib.colors as colors
ox.config(use_cache=True, log_console=True)
ox.__version__

place = {'city' : 'Hino',
         'state' : 'Tokyo',
         'country' : 'Japan'}

#network_type (string {"all_private", "all", "bike", "drive", "drive_service", "walk"}) 
G = ox.graph_from_place(place, network_type='bike')
fig, ax = ox.plot_graph(G)
fig.savefig("hino_bike.png")
```
## 参考
- [世界各都市の道路が向いている方角が可視化されたグラフを比べてみると何がわかるのか？ - GIGAZINE](https://gigazine.net/news/20180714-city-street-orientations/)
- [osmnx – OSMnx：街路網用のPython。 OpenStreetMapからストリートネットワークを取得、構築、分析、視覚化](https://githubja.com/gboeing/osmnx)
- [PythonのOSMnxパッケージを使って地図を可視化してみよう【初心者向け】](https://sinyblog.com/python/osmnx-001/)
- [OpenStreetMap Japan](https://openstreetmap.jp/#zoom=5&lat=38.06539&lon=139.04297&layers=B000)
