import requests, os, sys, pygame
from POI_TTS import poi_tts
from POI_STT import main as stt_main
from local_config import positive_responses, negative_responses, Tmap_key

import requests, urllib, pprint

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

        #yes_answer = any(response in choice.lower() for response in positive_responses)
        #no_answer = any(response in choice.lower() for response in negative_responses)
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


pygame.quit()

print(choice_name, choice_lat, choice_lon)    


route_url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

headers = {
    "Accept": "application/json",
    "appKey": Tmap_key
}

my_lon = 127.12879180000004
my_lat = 37.459713500071885

route_params = {
    "startX": my_lon,#내 위치 받도록 수정해야함#경도
    "startY": my_lat,#내 위치 받도록 수정해야함#위도
    "angle": 20,
    "speed": 1,
    "endX": choice_lon,
    "endY": choice_lat,
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