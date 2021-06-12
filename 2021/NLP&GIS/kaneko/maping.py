# -*- coding: utf-8 -*-

import folium
import select_data_csv
import geocoding
import time

search_string = input('検索する観光地: ')
data = select_data_csv.select_data(search_string)
if data[3] != "None":
    ido,keido = select_data_csv.loc_strtoval(data[3])
elif data[4] != "None":
    if data[5] == "緯度経度情報アリ":
        ido,keido = select_data_csv.loc_strtoval(data[4])
    else:
        ido,keido = geocoding.coordinate(data[4])
        #time.sleep(1)
    #print(ido,keido,data[0],"img/"+data[0]+"_freq.png")
    #exit()
else:
    print("exit")
    exit()

# 都立大日野キャンパスの緯度経度
start_loc = [35.661579,139.366468]
# 地図生成
folium_map = folium.Map(location=start_loc,zoom_start=10)

# マーカープロット
folium.Marker(popup="都立大",location=start_loc).add_to(folium_map)
folium.Marker(location=[ido, keido],popup='<a href="http://maps.google.com/maps?q=&layer=c&cbll=%d, %d&cbp=11,0,0,0,0">%s <br/><img width="60" src="%s">></a>' % (ido,keido,data[0],"./img/"+data[0]+"_freq.png")).add_to(folium_map)
loc_name,loc_ido,loc_keido = select_data_csv.search_min_dist_loc(float(start_loc[0]),float(start_loc[1]),float(ido),float(keido))
folium.Marker(
    location=[loc_ido, loc_keido],
    popup=loc_name,
    icon=folium.Icon(color='red', icon='home')
).add_to(folium_map)

#folium.line(locations=start_loc)
#folium_map.simple_marker([ido,keido], popup=data[0])
#inline_map(m)
folium.PolyLine(locations=[start_loc, [ido,keido]], color='blue').add_to(folium_map)

# 地図表示
#folium_map
folium_map.save('output.html')
