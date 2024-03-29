from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from gps_data import *

app = Flask(__name__)
socketio = SocketIO(app)

# 设置跨域
CORS(app, supports_credentials=True)

carData = []
carSpeed = []
# 路由，接收从嵌入式设备发送过来的数据
@app.route('/data', methods=['POST'])
def receive_data():
    global carData, carSpeed
    receive_data = request.get_json()
    send_data = run(receive_data)
    # keys_string = ", ".join(data.keys())    
    # if carData:
        
    # else:
    #     addTime(data)
    #     data[keys_string]['flag'] = 0
    #     carData.append(data)
    # 把data加入carData
    # 将数据通过 WebSocket 发送给 HTML 页面
    socketio.emit('device_data', send_data)
    return 'Data received and sent to clients'

# HTML 页面
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket 事件处理器
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
