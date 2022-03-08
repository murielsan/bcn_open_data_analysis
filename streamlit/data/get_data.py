import requests
import streamlit as st

# Direccion de nuestra API
url = "http://127.0.0.1:8000"

def get_stations_list():
    return requests.get(url+"/list_stations").json()

def get_station_info(name):
    return requests.get(url+f"/stations/{name}").json()

@st.experimental_memo
def get_station_measures_st(name, year, month, day):
    return requests.get(url+f"/stations/{name}/measures/{year}/{month}/{day}").json()

def get_stats_pokemon(name):
    return requests.get(url+f"/pokemon/stats/{name}").json()