from fastapi import APIRouter
from bson import json_util
from json import loads
from models.Measure import Measure
from database.mongo import get_data

# Population endpoint
router = APIRouter()

# Get stations list
@router.get("/list_bicing_stations")
def get_station_list():
    res = get_data('bicing')
    return loads(json_util.dumps(res))

@router.get("/get_bicing_stations_near/{lon}/{lat}/{radio}")
def get_stations_near(lon: float, lat: float, radio: int):
    geo_json = {
        "Location":{
            "$near":{            
                "$geometry":{
                    "type":"Point",
                    "coordinates":[lon,lat]
                },
            "$maxDistance":radio
            }
        }
    }
    res = get_data("bicing",geo_json)
    return loads(json_util.dumps(res))
