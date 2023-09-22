import requests

data  = requests.post('http://127.0.0.1:5000/lab1', json = {"data" : "33"})

print(data.text) 
print(data.status_code)