from json import loads

from bson import json_util
from database.mongo import (aggregation, distinct, get_data, insert_one_data,
                            insert_one_with_pass)
from fastapi import APIRouter, Header
from models.Measure import Measure
from utils.utils import get_air_quality

error_message = {"message": "No data found"}

# Population endpoint
router = APIRouter()


# Get stations list
@router.get("/list_stations")
def get_station_list():
    res = distinct('pollution', 'Station')
    return loads(json_util.dumps(res))


# Get station info
@router.get("/stations/{name}")
def get_station_info(name: str):
    res = get_data('pollution', filter={'Station': name},
                   project={'Station': 1, 'Location': 1, 'District Name': 1,
                            'Neighborhood name': 1, '_id': 0},
                   limit=1)
    return loads(json_util.dumps(res[0]))


# All the measures from a station
@router.get("/stations/{name}/measures/")
def get_station_measures(name: str):
    res = get_data('pollution', filter={'Station': name})
    return loads(json_util.dumps(res))


# Measures from a station for a selected date
@router.get("/stations/{name}/measures/{year}/{month}/{day}")
def get_station_measures(name: str, year:int, month:int, day:int):
    try:
        res = get_data('pollution',
                       filter={'Station': name, 'Year': year,
                               'Month': month, 'Day': day})
        return loads(json_util.dumps(res))
    except Exception:
        return error_message


# Average measures from a specified station and year
@router.get("/stations/{name}/average/{year}")
def get_station_mean(name: str, year: int):
    try:
        pipe = [{
                '$match': {'Station': name, 'Year': year}
            },
            {
                '$group': {
                    "_id": None,
                    'O3_avg': {
                        '$avg': '$O3'
                    },
                    'NO2_avg': {
                        '$avg': '$NO2'
                    },
                    'PM10_avg': {
                        '$avg': '$PM10'
                    },
                    'Station': {
                        '$first': '$Station'
                    },
                    'Year':  {
                        '$first': '$Year'
                    }
                }
            },
            {
                '$project': {
                    '_id':0
                }
            }
            ]
        res = aggregation('pollution', pipe)
        return loads(json_util.dumps(list(res)))
    except Exception:
        return error_message    


# Average for a station on a specific month
@router.get("/stations/{name}/average/{year}/{month}")
def get_station_mean(name: str, year: int, month: int):
    try:
        pipe = [{
                '$match': {'Station': name, 'Year': year, 'Month': month}
            },
            {
                '$group': {
                    "_id": None,
                    'O3_avg': {
                        '$avg': '$O3'
                    },
                    'NO2_avg': {
                        '$avg': '$NO2'
                    },
                    'PM10_avg': {
                        '$avg': '$PM10'
                    },
                    'Station': {
                        '$first': '$Station'
                    },
                    'Year':  {
                        '$first': '$Year'
                    },
                    'Month': {
                        '$first': '$Month'
                    }
                }
            },
            {
                '$project': {
                    '_id':0
                }
            }
            ]
        res = aggregation('pollution', pipe)
        return loads(json_util.dumps(list(res)))
    except Exception:
        return error_message


# Insert new measure, according to Measure class
@router.post("/new_measure/")
async def insert_measure(measure: Measure, user: str = Header(None), password: str = Header(None)):
    # Check if user and password have been specified
    if not user or not password:
        return {"message":"Invalid user or password"}
    
    # Check if already inserted by station and hour of the day
    if len(get_data("pollution",
                    filter={'Station': measure.station, 'Hour': measure.hour,
                            'Year': measure.year, 'Month': measure.month,
                            'Day': measure.day})) == 0:
        
        # Get the rest of the data from the database
        res = get_data('pollution',
                       filter={'Station': measure.station},
                       limit=1)
        if len(res) > 0:
            try:
                measure.location = res[0]['Location']
                measure.district = res[0]['District Name']
                measure.nbhood = res[0]['Neighborhood Name']
                measure.air_quality = get_air_quality(
                                        measure.o3,
                                        measure.no2,
                                        measure.pm10
                                        )
            except Exception:
                return {"Error": "Couldn't find station data on database"}

        inserted = insert_one_with_pass(user, password, "pollution", measure.dict(by_alias=True))
        if not inserted:
            return {"message":"Couldn't connect to database"}

        return {"message": "Measure inserted correctly",
                "id": str(inserted.inserted_id)}
    return {"message": "Data already in the database"}
