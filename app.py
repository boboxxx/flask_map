from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from gps_data import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up CORS
CORS(app, supports_credentials=True)

carData = []
carSpeed = []
# Route to receive data from embedded devices
@app.route('/data', methods=['POST'])
def receive_data():
    global carData, carSpeed
    receive_data = request.get_json()
    if receive_data:
        print(receive_data)
        # send_data = run(receive_data)
        socketio.emit('device_data', receive_data)

        return 'Data received and sent to clients'
    else:
        return 'Data is null'

# HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handler
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)
