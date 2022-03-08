from tokenize import String
from fastapi import APIRouter
from bson import json_util
from json import loads
from database.mongo import get_data, insert_one_data, distinct
from models.Measure import Measure

# Population endpoint
router = APIRouter()

# Get stations list
@router.get("/list_stations")
def get_station_list():
   res = distinct('pollution','Station')
   return loads(json_util.dumps(res))

# Get station info
@router.get("/stations/{name}")
def get_station_info(name):
   res = get_data('pollution',filter={'Station':name},project={'Station':1,'Location':1,'District Name':1,'Neighborhood name':1,'_id':0},limit=1)
   return loads(json_util.dumps(res[0]))

# Measures from a station for a selected date
@router.get("/stations/{name}/measures/{year}/{month}/{day}")
def get_station_measures(name, year, month, day):
   try:
      res = get_data('pollution',filter={'Station':name, 'Year':int(year), 'Month':int(month), 'Day':int(day)})
      return loads(json_util.dumps(res))
   except Exception as e:
      return {"message":"No data found"}

# All the measures from a station
@router.get("/stations/{name}/measures/")
def get_station_measures(name):
   res = get_data('pollution',filter={'Station':name})
   return loads(json_util.dumps(res[0]))

# Insert new measure, according to Measure class
@router.post("/insert/measure")
async def insert_measure(measure:Measure):
   # Check if already inserted by station and hour of the day
   if len(get_data("pollution", filter={'Station':measure.station, 'Hour':measure.hour, 'Year':measure.year, 'Month':measure.mont, 'Day':measure.day})) == 0:
      inserted = insert_one_data(measure)
      return {"message":"Measure inserted correctly", "id":str(inserted.inserted_id)}
   return {"message":"Data already in the database"}