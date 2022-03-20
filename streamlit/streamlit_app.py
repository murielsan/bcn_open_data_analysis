import streamlit as st
from datetime import date
from pages.air_quality import show_air_quality
from pages.new_air_measure import new_air_measure
from pages.bicing import bicing

# This is needed to preserve session_state in the cloud. Not locally.
st.session_state.update(st.session_state)

# Page manes
page_air_quality = 'Air Quality'
page_new_measure = 'New air measure'
page_bicing = 'Bicing'
page_contact = 'Contact'

# Page configuration
st.set_page_config(
    page_title="BCN Open Data Analysis",
    page_icon="bcn_logo.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)

# Default session_state
if 'active_page' not in st.session_state:
    st.session_state.active_page = page_air_quality
    st.session_state.radiobuttons = page_air_quality


# Code of contact page
def contact():
    st.title('Contact')
    st.write('Jorge Muriel')
    st.write('GitHub: https://github.com/murielsan/bcn_open_data_analysis')


# Callback functions
def cb_radio_button():
    st.session_state.active_page = st.session_state.radiobuttons


# Page selection
st.sidebar.radio(
            'Page Navigation', [page_air_quality, page_new_measure, page_bicing, page_contact],
            key='radiobuttons', on_change=cb_radio_button
            )


# Run the active page
if st.session_state.active_page == page_air_quality:
    show_air_quality()
elif st.session_state.active_page == page_new_measure:
    new_air_measure()
elif st.session_state.active_page == page_bicing:
    bicing()
elif st.session_state.active_page == page_contact:
    contact()
