import streamlit as st
from datetime import date
from data.api_mgr import get_stations_list, set_new_measure

def new_air_measure():

    st.title("Upload new data")
    stations = get_stations_list()

    st.write("Please, fill the form:")        
    col1, col2, col3 = st.columns([2,2,3])
    with col1:        
        dt = st.date_input("Date of the measure", max_value=date.today())
    with col2:
        hour = st.number_input("Hour", min_value=0, max_value=23)
    with col3:
        station = st.selectbox("Measure station",stations)

    col4, col5, col6 = st.columns(3)
    with col4:
        o3 = st.number_input("O3", value=0.0)
    with col5:
        no2 = st.number_input("NO2", value=0.0)
    with col6:
        pm10 = st.number_input("PM10", value=0.0)
    
    # Every form must have a submit button.
    if st.button("Submit"):
        st.write(station, hour, dt.year, dt.month, dt.day, o3, no2, pm10)
        set_new_measure(station, hour, dt.year, dt.month, dt.day, o3, no2, pm10)
