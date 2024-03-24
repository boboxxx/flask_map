# Flask后端代码
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/car1', methods=['POST'])
def receive_data():
    # 获取JSON数据
    data = request.get_json()
    print(data)
   
    return jsonify({data: 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=5000)
