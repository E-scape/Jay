import requests
import time
from function import *
from POI_TTS import poi_tts
from config import *


# GPS 스레드 시작
gps_thread = GPSPoller()
gps_thread.start()

# 초기 위치 설정 (실제 GPS 데이터로 대체)
print("GPS 값을 불러옵니다")
while True:
    my_lat, my_lon = get_current_position(gps_thread)
    if my_lat is not None and my_lon is not None:
        print(f"초기 GPS 위치: 위도 {my_lat}, 경도 {my_lon}")
        break
    else:
        print("GPS 신호를 기다리는 중...")
        time.sleep(1)

route_url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

headers = {
    "Accept": "application/json",
    "appKey": Tmap_key
}


route_params = {
    "startX": my_lon,
    "startY": my_lat,
    "angle": 20,
    "speed": 1,
    "endX": 127.1283993123593,  # 동서울대 학생회관
    "endY": 37.45838307122894,  # 동서울대 학생회관
    "reqCoordType": "WGS84GEO",
    "startName": "%EB%82%B4%EC%9C%84%EC%B9%98",
    "endName": "%EB%AA%A9%EC%A0%81%EC%A7%80",
    "searchOption": "0",
    "resCoordType": "WGS84GEO",
    "sort": "index"
}

route_response = requests.post(route_url, json=route_params, headers=headers)

index_list = []
description_list = []
coordinates_list = []

if route_response.status_code == 200:
    routedata = route_response.json()
    for feature in routedata["features"]:
        if feature["geometry"]["type"] == "Point":
            description = feature["properties"]["description"]
            coordinates = feature["geometry"]["coordinates"]
            index = feature["properties"]["index"]
            description_list.append(description)
            coordinates_list.append(coordinates)
            index_list.append(index)

    for i, (description, coordinates) in enumerate(zip(description_list, coordinates_list)):
        print(f"{description} {coordinates}")
    
    print("gps 좌표 2번째 찾는중")



    for x in range(len(description_list)):#안내점 리스트 요소의 개수만큼 반복
        poi_tts(f"{description_list[x]}", f"{description_list[x]}")

        target_lon, target_lat = map(float, coordinates_list[x+1])
        print(f"안내점 좌표: {target_lon}, {target_lat}")

        float(now_lat), float(now_lon) = get_current_position(gps_thread)

        total_distance = haversine(now_lat, now_lon, target_lat, target_lon)
        print(f"안내점까지의 전체 거리: {total_distance:.2f} 미터")

        next_announcement_distance = total_distance - 30

        now_lat = 0
        now_lon = 0

        while True:
            now_lat, now_lon = get_current_position(gps_thread)

            if now_lat is None or now_lon is None:#GPS 좌료를 인식 할 수 없을 때
                print("GPS 신호를 찾을 수 없습니다. 다시 시도합니다.")                                                              
                poi_tts("GPS 신호를 찾을 수 없습니다.", "GPS 신호를 찾을 수 없습니다")
                time.sleep(1)
                continue

            else:#GPS 좌표를 인식하면
                now_lat, now_lon = float(now_lat), float(now_lon)
                print(f"안내점 좌표: {target_lat}, {target_lon}")
                print(f"내 좌표 : {now_lat}, {now_lon}\n")
                
                distance_to_target = haversine(now_lat, now_lon, target_lat, target_lon)
                print(f"남은 거리: {distance_to_target:.2f} 미터")

                if distance_to_target <= next_announcement_distance:
                    poi_tts(f"다음 안내점까지 {int(distance_to_target)}미터 남았습니다.", f"다음 안내점까지 {int(distance_to_target)}미터 남았습니다.")
                    # 다음 알림 거리 설정 (30m 간격)
                    next_announcement_distance = distance_to_target - 30

                if check_proximity(now_lat, now_lon, target_lat, target_lon):#현재위치와 안내점의 좌표가 10m 이내이면 break
                    break

                time.sleep(0.05)  # 더 짧은 간격으로 위치 체크

else:
    print(f"Error: {route_response.status_code}")

# 프로그램 종료 시 GPS 스레드 정지
gps_thread.stop()
gps_thread.join()