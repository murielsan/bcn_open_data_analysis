from pydantic import BaseModel
from typing import Optional

# Creamos un modelo para la clase Pokemon. Todo parametro que no se
# encuentre aqui, será ignorado, y si falta alguno de ellos, ocurrirá
# un error y se indicará que falta el parametro.
class Measure(BaseModel):
    station:str
    hour:int
    year:int
    month:int
    day:int
    o3:Optional[float]
    no2:Optional[float]
    pm10:Optional[float]
    longitude:float
    latitude:float
    district:Optional[str]
    neighborhood:Optional[str]