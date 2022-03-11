from fastapi import APIRouter
from bson import json_util
from json import loads
from models.Measure import Measure
from database.mongo import get_data, insert_one_data, distinct
from utils.utils import get_air_quality



# Population endpoint
router = APIRouter()


# Get stations list
@router.get("/list_stations")
def get_station_list():
    res = distinct('pollution', 'Station')
    return loads(json_util.dumps(res))


# Get station info
@router.get("/stations/{name}")
def get_station_info(name):
    res = get_data('pollution', filter={'Station': name},
                   project={'Station': 1, 'Location': 1, 'District Name': 1,
                            'Neighborhood name': 1, '_id': 0},
                   limit=1)
    return loads(json_util.dumps(res[0]))


# All the measures from a station
@router.get("/stations/{name}/measures/")
def get_station_measures(name):
    res = get_data('pollution', filter={'Station': name})
    return loads(json_util.dumps(res[0]))


# Measures from a station for a selected date
@router.get("/stations/{name}/measures/{year}/{month}/{day}")
def get_station_measures(name, year:int, month:int, day:int):
    try:
        res = get_data('pollution',
                       filter={'Station': name, 'Year': year,
                               'Month': month, 'Day': day})
        return loads(json_util.dumps(res))
    except Exception:
        return {"message": "No data found"}


# Insert new measure, according to Measure class
@router.post("/new_measure/")
async def insert_measure(measure: Measure):
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
            except:
                return {"Error": "Couldn't find station data on database"}

        inserted = insert_one_data("pollution", measure.dict())
        return {"message": "Measure inserted correctly",
                "id": str(inserted.inserted_id)}
    return {"message": "Data already in the database"}
