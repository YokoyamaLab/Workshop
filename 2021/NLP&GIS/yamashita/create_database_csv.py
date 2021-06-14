# postgresqlに格納するcsvを作成するプログラム
# 横はspotid, title, lead, overview, latlon, address
# latlonとaddressの両方があるものは弾く
#! 不足しているデータは手で整形する

# できたら下のコマンドをpsqlで実行
# \copy wikidata from 'C:\Users\youse\OneDrive - Tokyo Metropolitan University\seminar\practice\practice_alg_nlp/wikidata.csv' with csv

import csv
import geocoder
import re

# 緯度経度情報がdmsの場合，degに変換する
def dms_to_deg(dms):
    d=re.findall(r'l(.*?)d+',dms)
    m=re.findall(r'd(.*?)m+',dms)
    s=re.findall(r'm(.*?)s+',dms)

    deg=[0.0,0.0]
    if len(d)!=2 or len(m)!=2 or len(s)!=2:
        return deg
    for i in range(2):
        deg[i]=float(d[i])+float(m[i])/60+float(s[i])/3600
    return deg

# 緯度経度情報を整形して渡す（なければ住所から求めて渡す）
def split_latlon(latlon, address):
    if latlon == 'None' and address != None:
        ret = geocoder.osm(address, timeout=5.0)
        latlon_list = ret.latlng
        if latlon_list==None:
            latlon_list=[0.0,0.0]

    #もしdmsならdegに変換
    if '緯' in latlon:
        latlon=latlon.replace('北緯','l')
        latlon=latlon.replace('東経',' l')
        latlon=latlon.replace('度','d')
        latlon=latlon.replace('分','m')
        latlon=latlon.replace('秒','s')
        latlon_list=dms_to_deg(latlon)

    if len(latlon_list)==2:
        return float(latlon_list[0]),float(latlon_list[1])
    else:
        return 0.0,0.0

if __name__ == '__main__':

    # csv input
    src = open('wikidata3_hand.csv', 'r', encoding='ms932')
    data = csv.reader(src, delimiter=',',doublequote=True, lineterminator='\r\n',quotechar='"', skipinitialspace=True)
    # csv output
    out = open('wikidata.csv', 'w',newline='')
    data_out = csv.writer(out, delimiter=',',doublequote=True, lineterminator='\r\n',quotechar='"', skipinitialspace=True)

    spotid=0
    for spot in data:

        title       = spot[0]
        lead        = spot[1]
        overview    = spot[2]
        latlon      = spot[3]
        address     = spot[4]
        print(title)

        if title == 'タイトル':
            continue
        if latlon == None and address == None:
            continue

        latitude, longitude = split_latlon(latlon, address)
        spotid+=1

        data_out.writerow([spotid,title,lead,overview,latitude,longitude,address])

    src.close()
    out.close()
