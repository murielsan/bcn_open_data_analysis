import streamlit as st
from pages.air_quality import show_air_quality
from pages.bicing import bicing
from pages.new_air_measure import new_air_measure

# This is needed to preserve session_state in the cloud. Not locally.
st.session_state.update(st.session_state)

# Page names
PAGE_AIR_QUALITY = "Air Quality"
PAGE_NEW_MEASURE = "New air measure"
PAGE_BICING = "Bicing"
PAGE_CONTACT = "Contact"

# Page configuration
st.set_page_config(
    page_title="BCN Open Data Analysis",
    page_icon="bcn_logo.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Default session_state
if "active_page" not in st.session_state:
    st.session_state.active_page = PAGE_AIR_QUALITY
    st.session_state.radiobuttons = PAGE_AIR_QUALITY


# Code of contact page
def contact():
    st.title("Contact")
    st.write("Jorge Muriel")
    st.write("GitHub: https://github.com/murielsan/bcn_open_data_analysis")


# Callback functions
def cb_radio_button():
    st.session_state.active_page = st.session_state.radiobuttons


# Page selection
st.sidebar.radio(
    "Page Navigation",
    [PAGE_AIR_QUALITY, PAGE_NEW_MEASURE, PAGE_BICING, PAGE_CONTACT],
    key="radiobuttons",
    on_change=cb_radio_button,
)


# Run the active page
if st.session_state.active_page == PAGE_AIR_QUALITY:
    show_air_quality()
elif st.session_state.active_page == PAGE_NEW_MEASURE:
    new_air_measure()
elif st.session_state.active_page == PAGE_BICING:
    bicing()
elif st.session_state.active_page == PAGE_CONTACT:
    contact()
