from fastapi import FastAPI
from funciones import get_top_5, generos_por_año, juegos_por_año, specs_por_año, earlyaccess_por_año, sentiment_por_año, metascore_por_año

app = FastAPI()

@app.get("/genero/{year}")
def genero(year: str):
    try:
        result = generos_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/juegos/{year}")
def juegos(year: str):
    try:
        result = juegos_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/specs/{year}")
def specs(year: str):
    try:
        result = specs_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/earlyaccess/{year}")
def earlyaccess(year: str):
    try:
        result = earlyaccess_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/sentiment/{year}")
def sentiment(year: str):
    try:
        result = sentiment_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/metascore/{year}")
def metascore(year: str):
    try:
        result = metascore_por_año(year)
        return result
    except Exception as e:
        return {"error": str(e)}