import requests

BASE = 'http://127.0.0.1:5000/api/'             # locally run Flask API
API_KEY = 'm8hd936ro04h9fq1'


# the (D)elete in CRUD
resp = requests.delete(BASE+'character/3', headers={'x-api-key': API_KEY})
print('delete:          ', resp)

# the (C)reate in CRUD
resp = requests.post(BASE+'character/3', {'name': 'Goku', 'level': 18}, headers={'x-api-key': API_KEY})
print('post:            ', resp.json())


# the (R)ecieve in CRUD
resp = requests.get(BASE+'character/3', headers={'x-api-key': API_KEY})
print('get (just #3):   ', resp.json())

resp = requests.get(BASE+'characters', headers={'x-api-key': API_KEY})
print('get (all):       ', resp.json())


# the (U)pdate in CRUD
resp = requests.put(BASE+'character/3', {'level': 20}, headers={'x-api-key': API_KEY})
print('put:             ', resp.json())