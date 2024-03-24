import requests

# 云服务器的URL
url = 'http://3.22.119.196:5000/data'

# 要发送的数据
data = {
    'latitude': '39.9042',
    'longitude': '116.4074'
}

# 发送POST请求

response = requests.post(url, json=data)

# 打印响应内容
print(response.text)
