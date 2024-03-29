def ddmmToDd(ddmm):
    # ddmm = float(ddmm)  # 先将字符串转换为浮点数
    degrees = int(ddmm / 100)  # 取整数部分作为度数  
    minutes = ddmm % 100       # 取余数作为分
    dd = degrees + minutes / 60  # 转换为十进制度格式
    return dd

def extract_data(data):
    parts = data.split(',')
    try:
        time_utc = parts[1]
        
        latitude = float(parts[2])
        lat_flag = parts[3]
        longitude = float(parts[4])
        lng_flag = parts[5]
    except (IndexError, ValueError):
        return None, None, None, None, None
    return time_utc, latitude, longitude, lat_flag, lng_flag

def is_north_or_east(data):
    return data not in {"S", "W"}

def run(data):
    coordinates_and_time = {}
    print("data:", data)
    print(type(data))
    gps_data = list(data.values())[0]
    carNumber = list(data.keys())[0]
    time_utc, latitude, longitude, lat_flag, lng_flag = extract_data(gps_data)
    if is_north_or_east(lat_flag):
        latitude = ddmmToDd(latitude)
    else:
        latitude = -ddmmToDd(latitude)
    if is_north_or_east(lng_flag):
        longitude = ddmmToDd(longitude)
    else:
        longitude = -ddmmToDd(longitude)
    coordinates_and_time.update({
        carNumber:{
        "time": time_utc,
        "latitude": latitude,
        "longitude": longitude
    }}
    )
    return coordinates_and_time

if __name__=='__main__':
    data =  {'car1': '$GPGGA,142249.40,5052.0980,N,00005.1207,W,1,08,18.65,116.36,M,45.442,M,,*42'}

    res = run(data)
    print(res)

