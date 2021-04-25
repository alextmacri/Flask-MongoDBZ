import requests

BASE = 'http://127.0.0.1:5000/'         # locally run Flask API


# the (C)reate in CRUD
resp = requests.post(BASE+'api/character/1', {'name': 'Goku'})
print(resp.json())


# the (R)ecieve in CRUD
resp = requests.get(BASE+'api/character/1')
print(resp.json())

resp = requests.get(BASE+'api/characters')
print(resp.json())


# the (U)pdate in CRUD
resp = requests.get(BASE+'api/character/1', {'name': 'Piccolo'})
print(resp.json())


# the (D)elete in CRUD
resp = requests.get(BASE+'api/character/1')
print(resp)