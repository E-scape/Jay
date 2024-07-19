import math

def cal_bearing(my_lat: float, my_lon: float, point_lat: float, point_lon: float):
    my_lat = math.radians(my_lat)
    my_lon = math.radians(my_lon)
    point_lat = math.radians(point_lat)
    point_lon = math.radians(point_lon)

    dlon = point_lon - my_lon

    y = math.sin(dlon) * math.cos(point_lat)
    x = math.cos(my_lat) * math.sin(point_lat) - math.sin(my_lat) * math.cos(point_lat) * math.cos(dlon)
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing

if __name__ == "__main__":
    a= cal_bearing(37.459713500071885, 127.12879180000004, 37.47063189999999, 127.12814550000007)
    cal_bearing()
    print(a)