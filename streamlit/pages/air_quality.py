import random
from datetime import date
from fileinput import filename

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st
import webcolors
from data.api_mgr import (get_station_info, get_station_measures_st,
                          get_stations_list)
from matplotlib.backends.backend_pdf import PdfPages
from utils.utils import send_email


def show_air_quality():

    st.title("BCN Open data analysis")
    st.text("Air Quality")
    stations = get_stations_list()

    # Select a different color for each station (saved to preserve)
    if 'colors' not in st.session_state:
        colors = {}
        # for s in range(len(stations)):
        # murielsan 22/03/20: Code quality improve
        for s, _ in enumerate(stations):
            # Choose a different defined color from webcolors dict
            colors[stations[s]] = webcolors.HTML4_HEX_TO_NAMES[
                                list(webcolors.HTML4_HEX_TO_NAMES.keys())[s]]
        st.session_state.colors = colors

    # Selector
    stations_selected = st.multiselect("Please, select a station", stations)    

    # Get station positions
    positions = pd.DataFrame(
                [get_station_info(x)['Location']['coordinates'] for x in stations_selected],
                columns=['lon', 'lat'])
    # Add station name
    positions['Station'] = [name for name in stations_selected]

    # Add a layer for each station
    color_layers = []
    for row in positions.iterrows():
        color_layers.append(
            pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame(
                    [[row[1]['lon'], row[1]['lat']]],
                    columns=['lon', 'lat']),
                get_position='[lon,lat]',
                get_fill_color=list(
                                webcolors.name_to_rgb(
                                    st.session_state.colors[row[1]['Station']])
                                    ),
                get_radius=200
            )
        )

    # Draw map
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state={"latitude": 41.3788,
                            "longitude": 2.1331, "zoom": 11, "pitch": 50},
        layers=color_layers,
    ))

    # Get air quality measures for each station
    dt = st.date_input(
                    "Measures date",
                    value=date(2018, 11, 1),
                    max_value=date.today())

    measures = []
    for stat in stations_selected:
        measures.append(pd.DataFrame(get_station_measures_st(
                                    stat, str(dt.year),
                                    str(dt.month), str(dt.day))))
    if measures:
        # Ignore index to avoid duplicates        
        measures = pd.concat(measures, ignore_index=True)
        # Set categorical order for Air Quality
        # measures['Air Quality'] = pd.Categorical(
        #                             measures['Air Quality'],
        #                             categories=['Good', 'Moderate', 'Poor'],
        #                            ordered=True)
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # A line plot for each measure
        fig1, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(
            x="Hour", y="O3", hue="Station",
            data=measures, ax=ax, palette=st.session_state.colors)
        ax.set_xticks(range(24))

        fig2,ax2 = plt.subplots(figsize=(10, 4))
        sns.lineplot(
            x="Hour", y="NO2", hue="Station",
            data=measures, ax=ax2, palette=st.session_state.colors)
        ax2.set_xticks(range(24))

        fig3,ax3 = plt.subplots(figsize=(10, 4))
        sns.lineplot(
            x="Hour", y="PM10", hue="Station",
            data=measures, ax=ax3, palette=st.session_state.colors)
        ax3.set_xticks(range(24))

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:  
        values = measures['Air Quality'].value_counts()
        labels = [x for x in values.keys()]
        sizes = [values.at[x] for x in values.keys()]

        fig4, ax4 = plt.subplots(figsize=(10, 4))
        ax4.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax4.axis('equal')
        
        
        col1.pyplot(fig1)
        col1.write('O3: less is better')
        col2.pyplot(fig2)
        col2.write('NO2: less is better')
        col3.pyplot(fig3)
        col3.write('PM10: less is better')
        col4.pyplot(fig4)
        col4.write('Air Quality: Percentage of quality hours')

        col5,col6 = st.columns([1,2])
        # Download button
        with col5:
            st.write('Get your results')
            # Create pdf file
            if 'pdf_rand_name' not in st.session_state:
                pdf_rand_name = f"Output{random.randint(0,65535)}.pdf"
                st.session_state.pdf_rand_name = pdf_rand_name

            pdf_file = PdfPages(st.session_state.pdf_rand_name)
            pdf_file.savefig(fig1)
            pdf_file.savefig(fig2)
            pdf_file.savefig(fig3)
            pdf_file.savefig(fig4)
            pdf_file.close()

            # Convert to binary
            with open(st.session_state.pdf_rand_name, 'rb') as f:
                fn = f"bcn_air_quality_{date.today()}.pdf"
                st.download_button("Save to PDF", f, file_name=fn)
        with col6:
            email = st.text_input("Email")
            if email:
                if st.button("Email PDF"):
                    send_email(email, st.session_state.pdf_rand_name)

        # Display dataframe
        st.text('Raw Data')
        st.dataframe(measures)
