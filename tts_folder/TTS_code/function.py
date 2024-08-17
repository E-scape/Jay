import math, time, threading
from gps3 import gps3

def cal_bearing(now_lat: float, now_lon: float, point_lat: float, point_lon: float) -> float:
    now_lat, now_lon, point_lat, point_lon = map(math.radians, [now_lat, now_lon, point_lat, point_lon])

    dlon = point_lon - now_lon

    y = math.sin(dlon) * math.cos(point_lat)
    x = math.cos(now_lat) * math.sin(point_lat) - math.sin(now_lat) * math.cos(point_lat) * math.cos(dlon)
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    두 좌표 (위도, 경도) 사이의 거리를 계산합니다.
    """
    R = 6371000  # 지구의 반지름 (미터)
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    delta_phi = lat2 - lat1
    delta_lambda = lon2 - lon1
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  # 미터 단위 거리
    return distance

def check_proximity(current_lat: float, current_lon: float, target_lat: float, target_lon: float, threshold: float = 10) -> bool:
    """
    현재 위치가 목표 좌표 근처(일정 거리 이내)에 있는지 확인합니다.
    """
    distance = haversine(current_lat, current_lon, target_lat, target_lon)
    print(f"거리: {distance}")
    return distance <= threshold

'''def get_current_position():
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()

    gps_socket.connect()
    gps_socket.watch()

    try:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                latitude = data_stream.TPV['lat']
                longitude = data_stream.TPV['lon']

                if latitude is not None and longitude is not None:
                    return float(latitude), float(longitude)
    except Exception as e:
        print(f"GPS 데이터를 가져오는 데 실패했습니다: {e}")
        return None, None
    finally:
        gps_socket.close()'''


class GPSPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gps_socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.running = True
        self.latitude = None
        self.longitude = None

    def run(self):
        self.gps_socket.connect()
        self.gps_socket.watch()
        for new_data in self.gps_socket:
            if not self.running:
                break
            if new_data:
                self.data_stream.unpack(new_data)
                lat = self.data_stream.TPV['lat']
                lon = self.data_stream.TPV['lon']
                if lat != 'n/a' and lon != 'n/a':
                    self.latitude = float(lat)
                    self.longitude = float(lon)
            time.sleep(0.05)  # 짧은 대기 시간으로 CPU 사용량 감소

    def stop(self):
        self.running = False

# 기존의 다른 함수들 (cal_bearing, haversine, check_proximity)은 그대로 유지

# get_current_position 함수는 이제 GPSPoller 객체를 인자로 받습니다
def get_current_position(gps_poller):
    lat, lon = gps_poller.latitude, gps_poller.longitude
    if lat is not None and lon is not None:
        return float(f"{lat:.5f}"), float(f"{lon:.5f}")
    return None, None


'''
if __name__ == "__main__":
    # 테스트 코드
    a = cal_bearing(37.459713500071885, 127.12879180000004, 37.47063189999999, 127.12814550000007)
    print(f"Bearing: {a}")

    b = check_proximity(37.46441167, 127.12940000, 37.48005586886674, 127.128979794898)
    print(f"Proximity check: {b}")'''

if __name__ == "__main__":
    #gps_thread = GPSPoller()
    #gps_thread.start()
    #
    #try:
    #    while True:
    #        lat, lon = get_current_position(gps_thread)
    #        if lat is not None and lon is not None:
    #            print(f"Current position: Latitude {lat}, Longitude {lon}")
    #        else:
    #            print("Waiting for GPS signal...")
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    gps_thread.stop()
    #    gps_thread.join()
    '''gps_thread = GPSPoller()
    gps_thread.start()
    
    try:
        while True:
            lat, lon = get_current_position(gps_thread)
            if lat is not None and lon is not None:
                print(f"Current position: Latitude {lat}, Longitude {lon}")
            else:
                print("Waiting for GPS signal...")
            time.sleep(1)
    except KeyboardInterrupt:
        gps_thread.stop()
        gps_thread.join()'''
    
    a= check_proximity(127.1289,37.459493333, 127.12899368732674,37.45955592769892)
    print(a)