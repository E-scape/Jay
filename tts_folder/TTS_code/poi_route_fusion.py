import requests, os, sys, pygame, time, requests, urllib, pprint
from function import *
from POI_TTS import poi_tts
from POI_STT import main as stt_main
from config import positive_responses, negative_responses, Tmap_key



pygame.init()
while True:
    
    stt_path = os.path.abspath(r"C:/Users/alsrn/projects/escape/tts_folder/TTS,STT_code/POI_STT.py")
    sys.path.append(stt_path)
    
    name_output =[]
    lat_output = []
    lon_output = []
    
    poi_url = "https://apis.openapi.sk.com/tmap/pois?version=1"
    
    #장소를 말하세요!
    location_value = stt_main()
    
    poi_params = {
        "searchKeyword": location_value, #stt로 받아온 값 넣기
        "searchType": "all",
        "searchtypCd": "A",         
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "page": "1",
        "count": "3",
        "multiPoint": "Y",
        "poiGroupYn": "N"
    }
    
    headers = {
        "Accept": "application/json",
        "appKey": Tmap_key
    }
    
    # Making the GET request with the params dictionary
    poi_response = requests.get(poi_url, headers=headers, params=poi_params)
    
    #에러코드
    if poi_response.status_code == 500:
        print("500 error")
        poi_tts("시스템 에러입니다.", "시스템에러입니다.mp3")
        break

    if poi_response.status_code == 400 or poi_response.status_code == 204:
        print(f"Error: {poi_response.status_code}")
        poi_tts("장소 검색에 실패했습니다. 다시 시도해 주세요.", "장소 검색에 실패했습니다 다시 시도해 주세요.mp3")
        location_value = ""
        continue

    # Checking the status code and printing the response
    if poi_response.status_code == 200:
        data = poi_response.json()

        search_data = data['searchPoiInfo']['pois']['poi']
        poi_count = int(data['searchPoiInfo']['count'])

        for poi in search_data:       #장소 검색 결과 출력
            목적지 = poi['name']
            front_lat = poi['frontLat']
            front_lon = poi['frontLon']

            #print(f"이름: {목적지}")
            #print(f"위도: {front_lat}, 경도: {front_lon}")
            #print("")

            name_output.append(목적지) #name_output에 name을 추가
            lat_output.append(front_lat) #lat_output에 lat을 추가
            lon_output.append(front_lon) #lon_output에 lon을 추가

        choice_name = ""
        choice_lat = ""
        choice_lon = ""
        choice = ""
        
        print(f"total_poi = {poi_count}")

        poi_tts(f"검색 결과, 총 {poi_count}개의 장소가 검색되었습니다.", "총 몇 개의 장소가 검색되었습니다.mp3")

        if poi_count == 1:#검색 결과가 1개일 때
            while True:
                poi_tts(f"{name_output[0]}으로 안내할까요?", "이장소로 안내할까요.mp3")#name_output에 있는 첫 번째 name을 말함
                choice = stt_main()

                #응답이 Yes일 때
                if any(response in choice.lower() for response in positive_responses):
                    choice_name = name_output[0]
                    choice_lat = lat_output[0]
                    choice_lon = lon_output[0]
                    print(choice_name, choice_lat, choice_lon)
                    break
                
                #응답이 No일 때 -> break -> else문으로 이동-> 장소 검색을 다시 함)
                elif any(response in choice.lower() for response in negative_responses):
                    poi_tts("다른 검색 결과가 없습니다. 목적지를 다시 말해주세요.", "결과가 없습니다 목적지를 다시 말해주세요.mp3")
                    break

                else:
                    poi_tts(f"응답을 이해하지 못했습니다.", "응답을 이해하지 못했습니다.mp3")
                    choice =""
                    continue  
            
            if choice_name=="":
                continue  
   
        if poi_count == 2:
            while True:
                poi_tts(f"{name_output[0]}으로 안내할까요?", "이장소로 안내할까요.mp3")#name_output에 있는 첫 번째 name을 말함
                choice = stt_main()

                #응답이 yes일 때
                if any(response in choice.lower() for response in positive_responses):
                    choice_name = name_output[0]
                    choice_lat = lat_output[0]
                    choice_lon = lon_output[0]
                    print(choice_name, choice_lat, choice_lon)
                    break
                
                #응답이 no일 때는 다음 장소로 안내하도록 함
                elif any(response in choice.lower() for response in negative_responses):
                    poi_tts(f"{name_output[1]}으로 안내할까요?", "이장소로 안내할까요.mp3")
                    choice = ""
                    choice = stt_main()
                    
                    #다음 장소가 목적지가 맞다면(응답이 Yes)
                    if any(response in choice.lower() for response in positive_responses):
                        choice_name = name_output[1]
                        choice_lat = lat_output[1]
                        choice_lon = lon_output[1]
                        print(choice_name, choice_lat, choice_lon)
                        break
                    
                    #
                    elif any(response in choice.lower() for response in negative_responses):
                        poi_tts("다른 검색 결과가 없습니다. 목적지를 다시 말해주세요.", "결과가 없습니다 목적지를 다시 말해주세요.mp3")
                        break

                else:
                    poi_tts("응답을 이해하지 못했습니다. 다시 말해 주세요.", "응답을 이해하지 못했습니다.mp3")
                    choice = stt_main()
                    continue

        if poi_count == 3:
            while True:
                poi_tts(f"{name_output[0]}으로 안내할까요?", "이장소로 안내할까요.mp3")#name_output에 있는 첫 번째 name을 말함
                choice = stt_main()

                if any(response in choice.lower() for response in positive_responses):
                    choice_name = name_output[0]
                    choice_lat = lat_output[0]
                    choice_lon = lon_output[0]
                    print(choice_name, choice_lat, choice_lon)
                    break

                elif any(response in choice.lower() for response in negative_responses):
                    poi_tts(f"{name_output[1]}으로 안내할까요?", "이장소로 안내할까요.mp3")
                    choice = ""
                    choice = stt_main()
                    if any(response in choice.lower() for response in positive_responses):
                        choice_name = name_output[1]
                        choice_lat = lat_output[1]
                        choice_lon = lon_output[1]
                        print(choice_name, choice_lat, choice_lon)
                        break

                    elif any(response in choice.lower() for response in negative_responses):
                        poi_tts(f"{name_output[2]}으로 안내할까요?", "이장소로 안내할까요.mp3")
                        choice = ""
                        choice = stt_main()
                        if any(response in choice.lower() for response in positive_responses):
                            choice_name = name_output[2]
                            choice_lat = lat_output[2]
                            choice_lon = lon_output[2]
                            print(choice_name, choice_lat, choice_lon)
                            break

                else:
                    poi_tts("죄송합니다. 응답을 이해하지 못했습니다. 다시 실행해 주세요.", "응답을 이해하지 못했습니다.mp3")
                    choice = stt_main()
                    continue    

        if choice_name:
            poi_tts(f"{choice_name}으로 안내를 시작합니다", "목적지로 안내를 시작합니다.mp3")
            url_encoding=urllib.parse.quote(choice_name)
            #my_lat, my_lon = ip_location()
            break
        else:
            continue #목적지 다시 입력받기


print(choice_name, choice_lat, choice_lon)    


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
    "startX": my_lon, #startX -> lon
    "startY": my_lat, #startY -> lat
    "angle": 20,
    "speed": 1,
    "endX":  choice_lon,# 목적지 
    "endY": choice_lat,  # 목적지
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

        now_lat, now_lon = get_current_position(gps_thread)
        now_lat, now_lon = float(now_lat), float(now_lon)

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
    
    pygame.quit()



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