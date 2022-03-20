from fastapi import FastAPI

from routers import air_quality_data, bicing

app = FastAPI()

# Indicamos a la API la localizacion de los otros endpoints, situados
# en otros archivos.
app.include_router(air_quality_data.router)
app.include_router(bicing.router)


@app.get("/")
async def root():
    return {"message": "BCN open data analysis API. Endpoints info: "
            "https://github.com/murielsan/bcn_open_data_analysis/"
            "blob/main/README.md"}
