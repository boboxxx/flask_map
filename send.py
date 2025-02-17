import requests
import time
import threading
from london_coordinates import get_oxford_street_coordinates

# 服务器URL
flask_server_url = "http://localhost:5002//data"

# 获取牛津街坐标点
oxford_coordinates = get_oxford_street_coordinates()

# 为两辆车准备数据，使用相同的坐标但不同的车辆ID
car1_data = [{'car1': coord} for coord in oxford_coordinates]
car2_data = [{'car2': coord} for coord in oxford_coordinates[::-1]]  # 反向行驶

def send_car_data(car_data, interval=0.3):
    index = 0
    while True:
        try:
            # 发送当前位置数据
            response = requests.post(url=flask_server_url, json=car_data[index])
            print(f"发送数据: {car_data[index]}")
            print(f"服务器响应: {response.text}")
            
            # 更新索引，循环发送数据
            index = (index + 1) % len(car_data)
            
            # 等待指定时间间隔
            time.sleep(interval)
            
        except requests.exceptions.RequestException as e:
            print(f"发送数据失败: {e}")
            time.sleep(1)  # 发生错误时等待1秒后重试

# 启动数据发送
if __name__ == "__main__":
    print("开始发送模拟数据...")
    try:
        # 创建两个线程分别发送car1和car2的数据
        thread1 = threading.Thread(target=send_car_data, args=(car1_data,))
        thread2 = threading.Thread(target=send_car_data, args=(car2_data,))
        
        # 启动线程
        thread1.start()
        thread2.start()
        
        # 等待线程结束（在这种情况下不会结束，除非发生KeyboardInterrupt）
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        print("\n数据发送已停止")
