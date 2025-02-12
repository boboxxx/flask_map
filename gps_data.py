def run(data):
    coordinates_and_time = {}
    print("data:", data)
    print(type(data))
    # 从输入数据中提取车辆编号和GPS数据
    car_data = list(data.values())[0]
    car_number = list(data.keys())[0]
    
    # 直接从JSON数据中获取经纬度
    latitude = car_data["latitude"]
    longitude = car_data["longitude"]
    
    # 构建返回数据结构，只包含经纬度信息
    coordinates_and_time.update({
        car_number: {
            "latitude": latitude,
            "longitude": longitude
        }
    })
    
    return coordinates_and_time

if __name__=='__main__':
    # 测试数据
    test_data = {
        'car1': {
            "latitude": 39.898457,
            "longitude": 116.391844,
            "flag": 1
        }
    }
    result = run(test_data)
    print(result)

