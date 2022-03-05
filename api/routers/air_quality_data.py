from tokenize import String
from fastapi import APIRouter
from database.mongo import get_data, insert_one_data, distinct
from bson import json_util
from json import loads

# Population endpoint
router = APIRouter()

@router.get("/list_stations")
def get_station_list():
   res = distinct('pollution','Station')
   return loads(json_util.dumps(res))