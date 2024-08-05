import math, time
from gps import *

def cal_bearing(now_lat: float, now_lon: float, point_lat: float, point_lon: float):
    now_lat = math.radians(now_lat)
    now_lon = math.radians(now_lon)
    point_lat = math.radians(point_lat)
    point_lon = math.radians(point_lon)

    dlon = point_lon - now_lon

    y = math.sin(dlon) * math.cos(point_lat)
    x = math.cos(now_lat) * math.sin(point_lat) - math.sin(now_lat) * math.cos(point_lat) * math.cos(dlon)
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing

def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    두 좌표 (위도, 경도) 사이의 거리를 계산합니다.
    """
    R = 6371000  # 지구의 반지름 (미터)
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  # 미터 단위 거리
    return distance

def check_proximity(current_lat: float, current_lon: float, target_lat: float, target_lon: float, threshold=5):
    """
    현재 위치가 목표 좌표 근처(일정 거리 이내)에 있는지 확인합니다.
    """
    distance = haversine(current_lat, current_lon, target_lat, target_lon)
    return distance <= threshold

def nav(now_lat: float, now_lon: float, point_lat: float, point_lon: float):
    
    pass


guide_points = [
    (37.45972535222696, 127.128979794898),
    (37.46005586886674, 127.12894923275134),
    (37.460030863863636, 127.12851038446631),
    # 더 많은 안내점을 추가할 수 있습니다.
]

'''def check_distance():
    current_location = get_current_location()
    print(f"현재 위치: 위도 {current_location[0]:.6f}, 경도 {current_location[1]:.6f}")
    
    for i, point in enumerate(guide_points):
        distance = haversine(current_location[0], current_location[1], point[0], point[1])
        print(f"안내점 {i+1}까지의 거리: {distance:.2f} 미터")
    
    print("\n")'''

def get_current_position():
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
    
    try:
        while True:
            report = gpsd.next()
            if report['class'] == 'TPV':
                latitude = getattr(report, 'lat', None)
                longitude = getattr(report, 'lon', None)
                
                if latitude is not None and longitude is not None:
                    return latitude, longitude
    except Exception as e:
        print(f"GPS 데이터를 가져오는 데 실패했습니다: {e}")
        return None, None


if __name__ == "__main__":
    a= cal_bearing(37.459713500071885, 127.12879180000004, 37.47063189999999, 127.12814550000007)
    print(a)
    b=check_proximity(127.12940000,37.46441167,127.128979794898,37,48005586886674)
    print(b)
    