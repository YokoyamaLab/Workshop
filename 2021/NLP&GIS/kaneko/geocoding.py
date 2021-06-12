# https://qiita.com/paulxll/items/7bc4a5b0529a8d784673
import requests
from bs4 import BeautifulSoup
import time
import tqdm


URL = 'http://www.geocoding.jp/api/'

# 住所から緯度経度を返す
def coordinate(address):
    payload = {'q': address}
    html = requests.get(URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    time.sleep(5)
    return [latitude, longitude]

# 住所のリストから緯度経度のリストを返す
def coordinates(addresses, interval=10, progress=True):
    coordinates = []
    for address in progress and tqdm(addresses) or addresses:
        coordinates.append(coordinate(address))
        time.sleep(interval)
    return coordinates

def main():
    addr = "東京都日野市旭が丘6-6"
    ido, keido = coordinate(addr)
    print(ido,keido)

if __name__ == "__main__":
    main()
