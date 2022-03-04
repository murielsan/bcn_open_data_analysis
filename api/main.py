from fastapi import FastAPI
from .routers import population

app = FastAPI()

# Indicamos a la API la localizacion de los otros endpoints, situados
# en otros archivos.
app.include_router(population.router)

@app.get("/")
async def root():
    return {"message":"BCN open data analysis API. Endpoints:\n"}