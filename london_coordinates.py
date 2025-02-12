# 伦敦牛津街(Oxford Street)的经纬度坐标点
# 从Marble Arch到Tottenham Court Road的主要节点

def get_oxford_street_coordinates():
    # 返回牛津街从西到东的一系列坐标点
    coordinates = [
        {"latitude": 51.5141, "longitude": -0.1589},  # Marble Arch
        {"latitude": 51.5142, "longitude": -0.1570},  # Oxford Street起点
        {"latitude": 51.5144, "longitude": -0.1545},  # Selfridges位置
        {"latitude": 51.5147, "longitude": -0.1520},  # Bond Street站
        {"latitude": 51.5149, "longitude": -0.1495},  # New Bond Street交叉口
        {"latitude": 51.5151, "longitude": -0.1470},  # Oxford Circus
        {"latitude": 51.5154, "longitude": -0.1445},  # Poland Street交叉口
        {"latitude": 51.5156, "longitude": -0.1420},  # Soho Street交叉口
        {"latitude": 51.5159, "longitude": -0.1395},  # Tottenham Court Road站
    ]
    return coordinates

def get_test_car_position(index=0):
    """获取测试车辆位置，index用于模拟车辆移动"""
    coordinates = get_oxford_street_coordinates()
    if index >= len(coordinates):
        index = 0
    return coordinates[index]