import pandas as pd
import pydeck as pdk
import streamlit as st
from data.api_mgr import get_bicing_stations_list, get_bicing_stations_near
from geopy.geocoders import Nominatim


def bicing():
    st.title("BCN Open data analysis")
    st.text("Bicing stations")

    bicing_stations = get_bicing_stations_list()
    stations_data = pd.DataFrame(bicing_stations)   
    positions = pd.DataFrame([row['coordinates'] for row in stations_data['Location']],
                        columns=['lon','lat']) 

    if 'near_station_pos' not in st.session_state:
        st.session_state.near_station_pos = None
        st.session_state.radio = 100
        st.session_state.longitude = 2.1667046
        st.session_state.latitude = 41.3839786

    near_stations = pd.DataFrame()
    st.session_state.radio = st.slider("Please select radio in meters", min_value=100, max_value=1000, step=50, value=100)
    addr = st.text_input("Please, introduce an address")

    geolocator = Nominatim(user_agent="bcn-open-data-st")
    if "Barcelona" not in addr:
        addr += ", Barcelona"
    location = geolocator.geocode(addr, country_codes='es')
    if location:
        st.session_state.latitude = location.latitude
        st.session_state.longitude = location.longitude
        near_stations = pd.DataFrame(get_bicing_stations_near(st.session_state.longitude, st.session_state.latitude, st.session_state.radio))
    else:
        near_stations = pd.DataFrame() # Empty DataFrame
    

    if not near_stations.empty:
        st.session_state.near_station_pos = pd.DataFrame([row['coordinates'] for row in near_stations['Location']],
                        columns=['lon','lat'])   

    # Draw map
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state={
                "latitude": st.session_state.latitude,
                "longitude": st.session_state.longitude,
                "zoom": 13,
                "pitch": 50
            },
            layers= [
                pdk.Layer(
                    'ScatterplotLayer',
                    data=positions,
                    get_position='[lon,lat]',
                    get_fill_color=[255,0,0],
                    get_radius=10
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=st.session_state.near_station_pos,
                    get_position='[lon,lat]',
                    get_fill_color=[0,255,0],
                    get_radius=10
                )                
                ],
        )
    )
