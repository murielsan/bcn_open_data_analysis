# BCN Open data analysis
This is a small and simple project to prove what we've learned at [CoreCode](https://www.corecode.school/en/bootcamp/big-data-machine-learning) bootcamp until now.<br>

It consists in a three part work:<br>
1. [Data cleaning](#Data-cleaning)
2. [Data access API](#Data-access-API)
3. [Data visualization](#Data-visualization)

## Data cleaning
You'll find it under the [*data*](./data/) folder.

I've selected *air quality data* and *bicing stations* for cleaning. It's been a hard job, as data provided is not well structured, contains lots of errors and a strange format.

*Air quality data* started with a csv from a [Kaggle set](https://www.kaggle.com/xvivancos/barcelona-data-sets), but got the most of the data from the [**Barcelona's City Hall Open Data Service**](https://opendata-ajuntament.barcelona.cat/en/), where you'll find loads of data to work with. There's an API to get the data but you can also download CSV files. I chose the API to apply `requests` library methods we learned. Please note that the format of both CSV and json data changed in 2019 so I had to create a dataset compatible with both formats.

For *Bicing Stations* I chose a CSV file, as it was faster and it's not an info constantly updated, so I downloaded the file and begun to work.

All the data has been uploaded to [MongoDB Atlas](https://www.mongodb.com/atlas/database), a cloud hosting for MongoDB.

You'll need [Jupyter Notebook](https://jupyter.org/) to work with this files, although [VSCode](https://code.visualstudio.com/) works great too.

## Data access API
You'll find it under the [*api*](./api/) folder.

We mainly used [fastapi](https://fastapi.tiangolo.com/) for this part. I've created a set of endpoints for each of the collections created in MongoDB:
- Pollution: for air quality data
- Bicing: for bicing stations

You'll find detailed explanation of the endpoints [below](#API-Endpoints).

The API has been uploaded to [Heroku](https://www.heroku.com/) and deployed inside a docker container.

## Data visualization
You'll find it under the [*streamlit*](./streamlit/) folder.

We've used [Streamlit](https://streamlit.io/) for this purpose. I've created a multi-page web app with queries to the API. The pages are detailed [below](#Streamlit-APP).

Streamlit app has also been uploaded to Heroku, but this time as a connection to a GitHub repo. As it's not a repo but a folder inside a repo, I had to add a [buildpack](https://github.com/timanovsky/subdir-heroku-buildpack) which allowed me to specify the folder I wanted to use.

In order to make streamlit work I also had to create a [Procfile](./streamlit/Procfile) file so that Heroku knows how to run this kind of app. I also had to create [runtime.txt](./streamlit/runtime.txt) as I'm using Python 3.10.2 and at the time of creation (March'22) the default runtime was Python 3.9.7. The file [requirements.txt](./streamlit/requirements.txt) specifies the libraries needed for building the application.


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
You **must** have write access to the database to be able to insert new elements. User and password must be provided in the headers:
```
{
    User: "your_db_user"
    Password: "your_db_password"
}
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
Find the nearest stations to the specified address! Use the slider to modify the search radio dinamically.

### Contact
Contact info
