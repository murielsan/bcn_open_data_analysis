import streamlit as st
from datetime import date
from pages.air_quality import show_air_quality
from pages.new_air_measure import new_air_measure

# This is needed to preserve session_state in the cloud. Not locally.
st.session_state.update(st.session_state)

# Page configuration
st.set_page_config(
    page_title="BCN Open Data Analysis",
    page_icon="bcn_logo.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)

# Default session_state
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Air Quality'
    st.session_state.slider1 = 0
    st.session_state.check1 = False
    st.session_state.radiobuttons = 'Air Quality'


# Code of contact page
def contact():
    st.title('Contact')
    st.write('Jorge Muriel')
    st.write('GitHub: https://github.com/murielsan/bcn_open_data_analysis')


# Callback functions
def CB_RadioButton():
    st.session_state.active_page = st.session_state.radiobuttons


# Page selection
st.sidebar.radio(
            'Page Navigation', ['Air Quality', 'New air measure', 'Contact'],
            key='radiobuttons', on_change=CB_RadioButton
            )


# Run the active page
if st.session_state.active_page == 'Air Quality':
    show_air_quality()
elif st.session_state.active_page == 'New air measure':
    new_air_measure()
elif st.session_state.active_page == 'Contact':
    contact()
