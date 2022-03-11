from pydantic import BaseModel, Field
from typing import Optional


# Measure model. We'll get the rest of the data from the database
class Measure(BaseModel):
    station: str = Field(alias="Station")
    hour: int = Field(alias="Hour")
    year: int = Field(alias="Year")
    month: int = Field(alias="Month")
    day: int  = Field(alias="Day")
    o3: Optional[float] = Field(alias="O3")
    no2: Optional[float] = Field(alias="NO2")
    pm10: Optional[float] = Field(alias="PM10")
    location: Optional[dict] = Field(alias="Location")
    district: Optional[str] = Field(alias="District Name")
    nbhood: Optional[str] = Field(alias="Neighborhood Name")
    air_quality: Optional[str] = Field(alias="Air Quality")
