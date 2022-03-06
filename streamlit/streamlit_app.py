import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from data.get_data import get_stations_list, get_station_pos

# This is needed to preserve session_state in the cloud. Not locally.
st.session_state.update(st.session_state)

# Page configuration
st.set_page_config(page_title="BCN Open Data Analysis", page_icon="bcn_logo.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

#--- Default session_state
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    st.session_state.slider1 = 0
    st.session_state.check1 = False
    st.session_state.radiobuttons = 'Home' 

#--- Code of each page
def home():
    st.title("BCN Open data analysis")
    st.text("Only Air Quality for the moment")
    data = get_stations_list()

    ls = st.multiselect("Selecciona una estación", data)
    positions = pd.DataFrame([get_station_pos(x)['Location']['coordinates'] for x in ls], columns=['lon','lat'])

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state={"latitude": 41.3788,
                            "longitude": 2.1331, "zoom": 11, "pitch": 50},
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=positions,
                get_position='[lon, lat]',
                get_color='[30,144,255, 160]',
                get_radius=200,
            ),
        ],
    ))

def slider():
    st.write('Welcome to the slider page')
    slide1 = st.slider('this is a slider',min_value=0,max_value=15,key='slider1' )    
    st.write('Slider position:',slide1)
    
def contact():
    st.title('Welcome to contact page')
    st.write(f'Multipage app. Streamlit {st.__version__}')
    if st.button('Click Contact'):
        st.write('Welcome to contact page')

#--- Callback functions
def CB_RadioButton():
    st.session_state.active_page = st.session_state.radiobuttons

#--- Page selection
st.sidebar.radio('Page Navigation', ['Home', 'Slider', 'Contact'], key='radiobuttons',on_change=CB_RadioButton)

#--- Run the active page
if   st.session_state.active_page == 'Home':
    home()
elif st.session_state.active_page == 'Slider':
    slider()
elif st.session_state.active_page == 'Contact':
    contact()