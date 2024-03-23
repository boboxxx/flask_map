from flask import Flask, render_template, make_response
import json, jsonify        
app = Flask(__name__)


@app.route('/index')
def index():
    data = {
        'name': 'John Doe',
        'age': 25
    }
    # response =  make_response(json.dumps(data, ensure_ascii=False))
    # response.mimetype = 'application/json'
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)