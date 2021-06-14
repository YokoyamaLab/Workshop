# 位置情報はwikidata_hand2.csvを参照
# wordcloudはtourist_spot.jsonを参照して作成してある

import folium
import re
from folium.map import Popup
from geopy import geocoders
from geopy.distance import geodesic
import base64
import webbrowser
import csv
import geocoder

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
        return [float(latlon_list[0]),float(latlon_list[1])]
    else:
        return 0.0,0.0

# 直線と各スポットの距離を求める
def calc_distance(search_point,departure_point,destination_point):
    a = destination_point[0] - departure_point[0]
    b = destination_point[1] - departure_point[1]
    a2 = a * a
    b2 = b * b
    r2 = a2 + b2
    tt = -(a*(departure_point[0]-search_point[0])+b*(departure_point[1]-search_point[1]))
    if tt<0:
        return (departure_point[0]-search_point[0])**2 + (departure_point[1]-search_point[1])**2
    if tt>r2:
        return (destination_point[0]-search_point[0])**2 + (destination_point[1]-search_point[1])**2
    f1 = a*(departure_point[1]-search_point[1])-b*(departure_point[0]-search_point[0])
    return (f1*f1)/r2

def main():
    src = open('wikidata3_hand.csv', 'r', encoding='ms932')
    data = csv.reader(src, delimiter=',',doublequote=True, lineterminator='\r\n',quotechar='"', skipinitialspace=True)

    departure_point=[35.6613427,139.3667929]
    destination_point=[0.0,0.0]
    search_point=[0.0,0.0]
    destination_title=input()
    # destination_title='東京都庁舎'
    search_title=''

    # 目的地のデータを確認してマーカー，直線をつける
    for spot in data:
        title = spot[0]
        latlon = spot[3]
        address = spot[4]

        if destination_title!=title:
            continue
        if latlon == None and address == None:
            continue

        destination_title=title
        destination_point=split_latlon(latlon,address)

    src.close()
    src = open('wikidata3_hand.csv', 'r', encoding='ms932')
    data = csv.reader(src, delimiter=',',doublequote=True, lineterminator='\r\n',quotechar='"', skipinitialspace=True)

    # 直線から最寄り他の目的地候補を探してマーカーをつける
    min_dis=float('inf')
    for spot in data:
        title = spot[0]
        latlon = spot[3]
        address = spot[4]

        if latlon == None and address == None:
            continue
        if title == 'タイトル':
            continue

        tmp_point=split_latlon(latlon,address)
        if tmp_point==[0.0,0.0]:
            print("can't get : "+title)
            continue

        dis=calc_distance(tmp_point,departure_point,destination_point)
        print(title,dis)
        if dis<min_dis and dis!=0.0:
            min_dis=dis
            search_point=tmp_point
            search_title=title

    dis=geodesic(departure_point,destination_point).km
    center_point=[(departure_point[0]+destination_point[0])/2,(departure_point[1]+destination_point[1])/2]

    # map
    folium_map = folium.Map(center_point,zoom_start=15-int(dis/5))
    # departure marker
    folium.Marker(location=departure_point,popup='departure',icon=folium.Icon(color='red',icon='home')).add_to(folium_map)
    # destination marker
    png='img/'+destination_title+'/'+'TFIDF.png'
    encoded=base64.b64encode(open(png,'rb').read()).decode()
    html='<img src="data:image/jpeg;base64,{}">'.format
    iframe=folium.IFrame(html(encoded), width=640, height=480)
    popup=folium.Popup(iframe, max_width=2650)
    folium.Marker(location=destination_point,popup=popup,icon=folium.Icon(color='red',icon='eye-open')).add_to(folium_map)
    # search marker
    print(search_title)
    png='img/'+search_title+'/'+'TFIDF.png'
    encoded=base64.b64encode(open(png,'rb').read()).decode()
    html='<img src="data:image/jpeg;base64,{}">'.format
    iframe=folium.IFrame(html(encoded), width=640, height=480)
    popup=folium.Popup(iframe, max_width=2650)
    folium.Marker(location=search_point,popup=popup,icon=folium.Icon(color='gray',icon='tag')).add_to(folium_map)
    # line
    line = folium.vector_layers.PolyLine(locations=[departure_point, destination_point], color='blue',weight=5)
    folium_map.add_child(line)

    # save & open
    folium_map.save('spots\mappingdata.html')
    browser=webbrowser.get('"C:\Program Files\Google\Chrome\Application\chrome.exe" %s')
    browser.open(r'C:\Users\youse\OneDrive - Tokyo Metropolitan University\seminar\practice\practice_alg_nlp\spots\mappingdata.html')

if __name__ == "__main__":
    main()
