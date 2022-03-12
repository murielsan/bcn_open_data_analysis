# BCN Open data analysis
Barcelona open data analysis mid-project

## Endpoints for the API
url: https://bcn-open-data-api.herokuapp.com/

**list_stations**:<br>
Returns a list of the stations which provide data

**stations/{name}**:<br>
Returns info for the station {name}, as from list_stations

**stations/{name}/measures/**:<br>
Returns all the measures from station {name}

**sstations/{name}/measures/{year}/{month}/{day}**:<br>
Returns measures from station {name} for the specified day

**/new_measure/**:<br>
POST command. Introduces a new measure into database<br>
Requires a dict with the following structure:<br>
```
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
        'Air Quality': string
    }
    *Required fields
```

## Streamlit APP
url: https://bcn-open-data-st.herokuapp.com/

### Air Quality
Select one or more stations. It will show the location of each station on the map, and the graphics for each measure (O3, NO2 and PM10) for each hour of the day.
It also shows the percentage of hours with Good, Moderate or Poor air quality

### New Measure
Fill the form to insert a new measure into the database

### Contact
Contact info
