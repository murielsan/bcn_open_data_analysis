# Extract data from csv files and load it into MongoDB Atlas
import pandas as pd

df = pd.read_csv("../downloads/air_stations_Nov2017.csv")
df.head()