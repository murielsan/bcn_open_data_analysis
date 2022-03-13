import requests
import streamlit as st

# Direccion de nuestra API
url = "https://bcn-open-data-api.herokuapp.com"


def get_stations_list():
    return requests.get(url+"/list_stations").json()


def get_station_info(name):
    return requests.get(url+f"/stations/{name}").json()


@st.experimental_memo
def get_station_measures_st(name, year, month, day):
    return requests.get(
            url+f"/stations/{name}/measures/{year}/{month}/{day}"
        ).json()

def set_new_measure(station, hour, year, month, day, o3, no2, pm10, user, password):
    ms = {
        'Station': station,
        'Hour': hour,        
        'Year': year,
        'Month': month,
        'Day': day,
        'O3': o3,
        'NO2': no2,
        'PM10': pm10}
    # Send authentication on header
    head = {
        'User': user,
        'Password': password
        }
    return requests.post(url+'/new_measure/', json=ms, headers=head)

def get_bicing_stations_list():
    return requests.get(url+"/list_bicing_stations").json()

def get_bicing_stations_near(lon, lat, radio):
    return requests.get(url+f"/get_bicing_stations_near/{lon}/{lat}/{radio}").json()