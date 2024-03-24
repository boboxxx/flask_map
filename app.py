# server.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

# 初始坐标
car1_coordinates = [
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

# 生成新坐标的函数
def generate_coordinates(interval, car_id):
    while True:
        time.sleep(interval)
        # 生成新的 GPS 坐标，此处仅做示例，您需要根据具体需求生成新坐标
        new_latitude = car1_coordinates[-1]["latitude"] + 0.001  # 示例：每次增加0.001
        new_longitude = car1_coordinates[-1]["longitude"] + 0.001  # 示例：每次增加0.001
        new_coordinate = {"latitude": new_latitude, "longitude": new_longitude}
        car1_coordinates.append(new_coordinate)
        socket_io.emit('from-server', {'carId': car_id, 'coordinates': [new_coordinate]})

# 定时生成新坐标的线程
thread1 = threading.Thread(target=generate_coordinates, args=(1, 'car1'))  # 每1秒生成一次坐标
thread2 = threading.Thread(target=generate_coordinates, args=(2, 'car2'))  # 每2秒生成一次坐标

def start_threads():
    thread1.start()
    thread2.start()

@socket_io.on('connect')
def handle_connect():
    print('new connection')
    start_threads()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socket_io.run(app, port=50000, debug=True)
