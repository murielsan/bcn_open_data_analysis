import streamlit as st
import geopy
import pandas as pd
import pydeck as pdk
from data.api_mgr import get_bicing_stations_list, get_bicing_stations_near

def bicing():
    st.title("BCN Open data analysis")
    st.text("Bicing stations")

    bicing_stations = get_bicing_stations_list()
    print(bicing_stations)
    data = pd.DataFrame(bicing_stations)    
    print(pd.head())

    # Draw map
    #st.pydeck_chart(pdk.Deck(
    #    map_style="mapbox://styles/mapbox/dark-v9",
    #    initial_view_state={"latitude": 41.3788,
    #                        "longitude": 2.1331, "zoom": 11, "pitch": 50},
    #    layers= pdk.Layer(
    #            'ScatterplotLayer',
    #            data=pd.DataFrame(
    #                [[row[1]['lon'], row[1]['lat']]],
    #                columns=['lon', 'lat']),
    #            get_position='[lon,lat]',
    #            get_fill_color=list(
    #                            webcolors.name_to_rgb(
    #                                st.session_state.colors[row[1]['Station']])
    #                                ),
    #            get_radius=200
    #        ),
    #))