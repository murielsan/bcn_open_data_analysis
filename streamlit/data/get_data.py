import requests

# Direccion de nuestra API
url = "http://127.0.0.1:8000"

def get_stations_list():
    return requests.get(url+"/list_stations").json()

def get_station_pos(name):
    return requests.get(url+f"/stations/{name}").json()

def get_stats_pokemon(name):
    return requests.get(url+f"/pokemon/stats/{name}").json()