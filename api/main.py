from fastapi import FastAPI
from routers import air_quality_data
import uvicorn

app = FastAPI()

# Indicamos a la API la localizacion de los otros endpoints, situados
# en otros archivos.
app.include_router(air_quality_data.router)

@app.get("/")
async def root():
    return {"message":"BCN open data analysis API. Endpoints info: https://github.com/murielsan/bcn_open_data_analysis/blob/main/README.md"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)