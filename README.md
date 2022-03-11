# BCN Open data analysis
Barcelona open data analysis mid-project

## Endpoints for the API
[link url] (https://bcn-open-data-api.herokuapp.com/)

**list_stations**:
Returns a list of the stations which provide data

**stations/{name}**
Returns info for the station {name}, as from list_stations

**stations/{name}/measures/**
Returns all the measures from station {name}

**sstations/{name}/measures/{year}/{month}/{day}**
Returns measures from station {name} for the specified day

**/new_measure/**
POST command. Introduces a new measure into database
Requires a dict with the following structure:
    {
        *'Station': string,
        *'Hour': integer,        
        *'Year': integer,
        *'Month': integer,
        *'Day': integer,
        'O3': float,
        'NO2': float,
        'PM10': float,
        'District Name': string,
        'Neighborhood Name': string,
        'Air Quality': string}
    }
*Required fields

## Streamlit APP
[link url] (https://share.streamlit.io/murielsan/bcn_open_data_analysis)

### Air Quality
Select one or more stations. It will show the location of each station on the map, and the graphics for each measure (O3, NO2 and PM10) for each hour of the day.
It also shows the percentage of hours with Good, Moderate or Poor air quality

### New Measure
Fill the form to insert a new measure into the database

### Contact
Contact info