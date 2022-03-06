from tokenize import String
from fastapi import APIRouter
from bson import json_util
from json import loads
from database.mongo import get_data, insert_one_data, distinct
from models.Measure import Measure

# Population endpoint
router = APIRouter()

@router.get("/list_stations")
def get_station_list():
   res = distinct('pollution','Station')
   return loads(json_util.dumps(res))

@router.get("/stations/{name}")
def get_station_list(name):
   res = get_data('pollution',filter={'Station':name},project={'Station':1,'Location':1,'District Name':1,'Neighborhood name':1,'_id':0},limit=1)
   return loads(json_util.dumps(res[0]))

# Insert new measure, according to Measure class
@router.post("/insert/measure")
async def insert_measure(measure:Measure):
   # Check if already inserted by station and hour of the day
   if len(get_data("pollution", filter={'Station':measure.station, 'Hour':measure.hour, 'Year':measure.year, 'Month':measure.mont, 'Day':measure.day})) == 0:
      inserted = insert_one_data(measure)
      return {"message":"Measure inserted correctly", "id":str(inserted.inserted_id)}
   return {"message":"Data already in the database"}