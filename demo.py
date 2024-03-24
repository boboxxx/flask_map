# Flask后端代码
from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gps-data')
def gps_data():
    # 假设这是从嵌入式设备接收到的GPS数据
    gps_data = {'latitude': 39.9042, 'longitude': 116.4074}
    return jsonify(gps_data)

if __name__ == '__main__':
    app.run(debug=True)
