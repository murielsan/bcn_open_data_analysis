# BCN Open data analysis
Barcelona open data analysis mid-project

# API Endpoints
url: https://bcn-open-data-api.herokuapp.com/

## Air Quality
### - **list_stations**:<br>
Returns a list of the stations which provide data

### - **stations/{name}**:<br>
Returns info for the station {name} from list_stations. Example:
```
    {
        "Station":"Sants",
        "District Name":"Sants-Montjuic",
        "Location":{
            "type":"Point",
            "coordinates":[2.1331,41.3788]
        }
    }
```

### - **stations/{name}/measures/**:<br>
Returns all the measures from station {name}. Example:
```
    {
        "Station":"Sants",
        "O3":0.0,
        "NO2":84.0,
        "PM10":0.0,
        "Hour":0,
        "Year":2018,
        "Month":11,
        "Day":1,
        "Air Quality":"Poor",
        "District Name":"Sants-Montjuic",
        "Neighborhood Name":"Sants",
        "Location":{
            "type":"Point",
            "coordinates":[2.1331,41.3788]
        }
    }
```

### - **stations/{name}/measures/{year}/{month}/{day}**:<br>
Returns measures from station {name} for the specified day. Example:
```
    [
        {"Station":"Sants","O3":0.0,"NO2":84.0,"PM10":0.0,"Hour":0,"Year":2018,"Month":11,"Day":1,"Air Quality":"Poor","District Name":"Sants-Montjuic","Neighborhood Name":"Sants","Location":{"type":"Point","coordinates":[2.1331,41.3788]}},
        {"Station":"Sants","O3":0.0,"NO2":62.0,"PM10":0.0,"Hour":1,"Year":2018,"Month":11,"Day":1,"Air Quality":"Moderate","District Name":"Sants-Montjuic","Neighborhood Name":"Sants","Location":{"type":"Point","coordinates":[2.1331,41.3788]}}
        ...
    ]
```

### - **stations/{name}/average/{year}**:<br>
Returns average measures from a Station for a specific year. Example:
```
    [
        {
            "O3_avg":0.0,
            "NO2_avg":33,
            "PM10_avg":0.0,
            "Station":"Sants",
            "Year":2018
        }
    ]
```

### - **stations/{name}/average/{year}/{month}**:<br>
Returns average measures from a Station for a specific month of the year. Example:
```
    [
        {
            "O3_avg":0.0,
            "NO2_avg":32.93769470404985,
            "PM10_avg":0.0,
            "Station":"Sants",
            "Year":2018,
            "Month":11
        }
    ]
```

### - **new_measure**:<br>
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
## Bicing stations
### - **list_bicing_stations**:<br>
Returns the complete list of bicing stations. Example:
```
    [
        {"Name":"Pl Tetuan, 15","Street name":"Pl Tetuan","Street number":15,"Neighborhood name":"la Dreta de l Eixample","District name":"Eixample","Zip code":8010,"Location":{"type":"Point","coordinates":[2.17475743146867,41.3946851545578]}},
        {"Name":"Pl Tetuan, 8","Street name":"Pl Tetuan","Street number":8,"Neighborhood name":"la Dreta de l Eixample","District name":"Eixample","Zip code":8010,"Location":{"type":"Point","coordinates":[2.17528363937079,41.3943067790178]}}
        ...
    ]
```

### - **get_bicing_stations_near/{lon}/{lat}/{radio}**:<br>
Returns the list of bicing stations in the specified radio(meters). Example:
```
    [
        {"Name":"Pl Tetuan, 15","Street name":"Pl Tetuan","Street number":15,"Neighborhood name":"la Dreta de l Eixample","District name":"Eixample","Zip code":8010,"Location":{"type":"Point","coordinates":[2.17475743146867,41.3946851545578]}},
        {"Name":"Pl Tetuan, 8","Street name":"Pl Tetuan","Street number":8,"Neighborhood name":"la Dreta de l Eixample","District name":"Eixample","Zip code":8010,"Location":{"type":"Point","coordinates":[2.17528363937079,41.3943067790178]}}
        ...
    ]
```

# Streamlit APP
url: https://bcn-open-data-st.herokuapp.com/

### Air Quality
Select one or more stations. It will show the location of each station on the map, and the graphics for each measure (O3, NO2 and PM10) for each hour of the day.
It also shows the percentage of hours with Good, Moderate or Poor air quality

### New Measure
Fill the form to insert a new measure into the database

### Bicing
Find the nearest stations to the specified address!

### Contact
Contact info
