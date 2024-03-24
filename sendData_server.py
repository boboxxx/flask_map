import requests
import time

# 云服务器的URL
url = 'http://3.22.119.196:5000/data'

# 要发送的数据
car1 = [
    {"latitude": 39.898457, "longitude": 116.391844},
    {"latitude": 39.898595, "longitude": 116.377947},
    {"latitude": 39.898341, "longitude": 116.368001},
    {"latitude": 39.898063, "longitude": 116.357144},
    {"latitude": 39.899095, "longitude": 116.351934},
    {"latitude": 39.905871, "longitude": 116.35067},
    {"latitude": 39.922329, "longitude": 116.3498},
    {"latitude": 39.931017, "longitude": 116.349671},
    {"latitude": 39.939104, "longitude": 116.349225},
    {"latitude": 39.942233, "longitude": 116.34991},
    {"latitude": 39.947263, "longitude": 116.366892},
    {"latitude": 39.947568, "longitude": 116.387537}
  ]
# 每秒发送car1的一组数据
for data in car1:
    response = requests.post(url, json=data)
    # 打印响应内容
    print(response.text)
    time.sleep(1)


