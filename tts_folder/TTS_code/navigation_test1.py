import requests, os, sys, pygame, time
from function import *
from POI_TTS import poi_tts
from POI_STT import main as stt_main
from config import *

route_url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

headers = {
    "Accept": "application/json",
    "appKey": Tmap_key
}

my_lon = 127.12879180000004
my_lat = 37.459713500071885

route_params = {
    "startX": my_lon, #내 위치 받도록 수정해야함#경도
    "startY": my_lat, #내 위치 받도록 수정해야함#위도
    "angle": 20,
    "speed": 1,
    "endX": 127.1283993123593, #동서울대 학생회관
    "endY": 37.45838307122894,  #동서울대 학생회관
    #경유지 : "passList": "126.92774822,37.55395475_126.92577620,37.55337145",
    "reqCoordType": "WGS84GEO",
    "startName": "%EB%82%B4%EC%9C%84%EC%B9%98",#내 위치
    "endName": "%EB%AA%A9%EC%A0%81%EC%A7%80",#목적지
    "searchOption": "0",
    "resCoordType": "WGS84GEO",
    "sort": "index"
}

route_response = requests.post(route_url, json=route_params, headers=headers)
         
index_list =[]
description_list = []
coordinates_list = []

if route_response.status_code == 200:
    routedata = route_response.json()
    #pprint.pprint(routedata)
    for feature in routedata["features"]:
        if feature["geometry"]["type"] == "Point":
            description = feature["properties"]["description"]
            coordinates = feature["geometry"]["coordinates"]
            index= feature["properties"]["index"]
            description_list.append(description)
            coordinates_list.append(coordinates)
            index_list.append(index)
            #print(description)

    for i in range(len(description_list)):
        print(description_list[i], coordinates_list[i])

        for x in range(len(description_list)):
            target_lat, target_lon = coordinates_list[x][1], coordinates_list[x][0]

            while True:
                my_lat, my_lon = get_current_position()
                if my_lat is None or my_lon is None:
                    print("GPS 신호를 찾을 수 없습니다. 다시 시도합니다.")
                    time.sleep(1)
                    continue

                if check_proximity(my_lat, my_lon, target_lat, target_lon):
                    if x + 1 < len(description_list):
                        poi_tts(f"{description_list[x+1]}", f"{description_list[x+1]}.mp3")
                    break
                
                time.sleep(3)  # 3초 대기 후 다시 검사

else:
    print(f"Error: {route_response.status_code}")

'''
class coordinate:
    def __init__(self):
        self.lat = None
        self.lon = None
    
    def set_coordinate(self, lat, lon):
        self.lat = lat
        self.lon = lon
        return self.lat, self.lon
    
'''