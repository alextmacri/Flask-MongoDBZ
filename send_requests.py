import requests

BASE = 'http://127.0.0.1:5000/api/'             # locally run Flask API


# the (D)elete in CRUD
resp = requests.delete(BASE+'character/3')
print('delete:          ', resp)

# the (C)reate in CRUD
resp = requests.post(BASE+'character/3', {'name': 'Goku', 'level': 18})
print('post:            ', resp.json())


# the (R)ecieve in CRUD
resp = requests.get(BASE+'character/3')
print('get (just #3):   ', resp.json())

resp = requests.get(BASE+'characters')
print('get (all):       ', resp.json())


# the (U)pdate in CRUD
resp = requests.put(BASE+'character/3', {'level': 20})
print('put:             ', resp.json())