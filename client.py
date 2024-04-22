import requests
import time


host ='http://127.0.0.1:5000'
#
response = requests.post(f'{host}/upscale/', json={'image_1': 'lama_300px.png',
                                                   'image_2': 'upscale1.png'},)
print(response.status_code)
print(response.json())

task_id = response.json().get('task_id')
print(task_id)


response = requests.get(f'{host}/tasks/{task_id}').json()
status = response['status']
print(status)

while status not in {'SUCCESS', 'FAILURE'}:
    time.sleep(7)
    response = requests.get(f'{host}/tasks/{task_id}').json()
    status = response['status']
    print(response)
