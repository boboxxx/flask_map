# server.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from time import time


app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

@app.route('/data', methods=['POST'])
def receive_data():
    # 获取JSON数据
    data = request.get_json()
    # 打印接收到的数据
    print(data)
    # 可以在这里添加数据处理逻辑
    # ...
    # 返回成功响应
    return jsonify({'status': 'success'}), 200

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

car2 =  [
    {"latitude": 39.947764, "longitude": 116.401988},
    {"latitude": 39.947929, "longitude": 116.410824},
    {"latitude": 39.947558, "longitude": 116.42674},
    {"latitude": 39.9397, "longitude": 116.427338},
    {"latitude": 39.932404, "longitude": 116.427919},
    {"latitude": 39.923109, "longitude": 116.428377},
    {"latitude": 39.907094, "longitude": 116.429583},
    {"latitude": 39.906858, "longitude": 116.41404},
    {"latitude": 39.906622, "longitude": 116.405321},
    {"latitude": 39.906324, "longitude": 116.394954},
    {"latitude": 39.906308, "longitude": 116.391264},
    {"latitude": 39.916611, "longitude": 116.390748}
  ]





def send_data():
    i = 0 
    while True:
        socket_io.sleep(0.3)
        data = {
            'car1': car1[i],
            'car2': car2[i]
        }
        socket_io.emit('from-server', data)
        i += 1  

        
    
    
@socket_io.on('connect')
def handle_connect():
    print('new connection')
    socket_io.start_background_task(send_data)

@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    socket_io.emit('from-server', send_data())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    socket_io.run(app, port=50000, debug=True)