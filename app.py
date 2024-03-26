from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)

# 全局变量，用于存储 POST 请求中的数据
car1 = None
car2 = None
# 设置跨域
CORS(app, supports_credentials=True)

@app.route('/data', methods=['POST', 'GET'])
def receive_data():
    global car1, car2
    if request.method == 'POST':
        # 获取 POST 请求中的数据
        data = request.json
        print('Received data:', data)

        # 检查数据中是否包含 'car1' 或 'car2' 键
        if 'car1' in data:
            car1 = data['car1']
            print('car1:', car1)
        elif 'car2' in data:
            car2 = data['car2']
            print('car2:', car2)
        else:
            return jsonify({"error": "Invalid data format"}), 400
        
        # 返回成功响应
        return jsonify({"message": "Data received successfully"})
    elif request.method == 'GET':
        # 如果是 GET 请求，返回相应的车辆数据
            if car1 and car2:
                return jsonify({"car1": car1, "car2": car2})
            elif car1:
                return jsonify({"car1": car1})
            elif car2:
                return jsonify({"car2": car2})
            else:
                return jsonify({"error": "No data available"}), 400
        

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
