import requests
import time

# 云服务器的URL
flask_server_url = "http://localhost:8080/data"

# 要发送的数据
# {'car1': [39, 116]}
# {'car2': [39, 116]}

# car1 = [{'car1':  
#     {"latitude": 39.898457, "longitude": 116.391844, "flag":1}},
#     {'car2':
#     {"latitude": 39.898595, "longitude": 116.377947, "flag":0}},
#      {'car2':
#     {"latitude": 39.898341, "longitude": 116.368001, "flag":1}},
#      {'car2':
#     {"latitude": 39.898063, "longitude": 116.357144, "flag":0}},
#      {'car2':
#     {"latitude": 39.899095, "longitude": 116.351934, "flag":0}},
#     #  {'car2':
#     # {"latitude": 39.905871, "longitude": 116.35067, "flag":0}},
#     #  {'car2':
#     # {"latitude": 39.922329, "longitude": 116.3498, "flag":1}}
# ]

car2 = [{'car2':
    {"latitude": 39.931017, "longitude": 116.349671, "flag": 0}},
{'car2':
    {"latitude": 39.939104, "longitude": 116.349225, "flag": 0}},
    {'car2':
    {"latitude": 39.942233, "longitude": 116.34991, "flag": 0}},
    {'car2':
    {"latitude": 39.947263, "longitude": 116.366892, "flag": 0}},
    {'car2':
    {"latitude": 39.947568, "longitude": 116.387537, "flag": 1}}
  ]

cnt = 0 

#同时发送两辆车的数据,每次只发送一条数据，
# eg:{'car2':[ {"latitude": 39.931017, "longitude": 116.349671, "flag": 0}}
while True:
    
        response = requests.post(url=flask_server_url, json=car2[cnt])
        print(response.text)
        print("sent data:", car2[cnt])
        cnt += 1      
        time.sleep(0.5)
        if cnt == len(car2) -1 :
                cnt = 0 
