from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
socket_io = SocketIO(app, cors_allowed_origins="*")


# 存储设备的 GPS 数据
device_gps_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('get_gps_data')
def send_gps_data():
    emit('gps_data', device_gps_data)

@app.route('/device1', methods=['POST'])
def receive_gps_data_from_device1():
    if request.method == 'POST':
        data = request.json  # 假设数据以 JSON 格式发送
        device_gps_data['device1'] = data
        socketio.emit('gps_data', device_gps_data)
        return "GPS received"

@app.route('/device2', methods=['POST'])
def receive_gps_data_from_device2():
    if request.method == 'POST':
        data = request.json  # 假设数据以 JSON 格式发送
        device_gps_data['device2'] = data
        socketio.emit('gps_data', device_gps_data)
        return "GPS received"

if __name__ == '__main__':
    socketio.run(app, debug=True, host = '0.0.0.0', port = 5000)
