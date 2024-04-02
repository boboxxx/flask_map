import requests
import time
import sysv_ipc

flask_url = 'http://ip/data'
key = 0x610600ed
mem_size =  4096
memory = sysv_ipc.SharedMemory(key, flags=sysv_ipc.IPC_CREAT, size=mem_size)
while True:

    memory_value = memory.read()
    memory_value = memory_value.rstrip(b'\x00')
    decoded_value = memory_value.decode('utf-8')
    data = {'car2': decoded_value}
    response = requests.post(url = flask_url, json = data)

    print('data:', data)
    print('response:', response.text)