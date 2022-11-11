import uvicorn
from fastapi import FastAPI

app = FastAPI()



d = {}
file = open("PLZO_CSV_LV95.csv", encoding="utf-8")
next(file)
for line in file:
    daten = line.strip().split(";")
    ort = daten [0]
    zip = daten[1]
    zusatz = daten[2]
    gemeinde = daten[3]
    bfs = daten[4]
    kanton = daten[5]
    E = daten[6]
    N = daten[7]
    sprache = daten[8]
    d[ort] = {"Ort": ort, "PLZ": zip, "Zusatzziffer": zusatz, "Gemeinde" : gemeinde, "BFS-Nummer": bfs, "Kanton": kanton, "E": E, "N": N, "Sprache": sprache}

file.close()

@app.get("/ort")
async def ort(ort : str ):
    
    if ort in d:
        return d[ort]
        
    return{"ERROR": "ORT NOT FOUND"}


uvicorn.run(app, host="127.0.0.1", port=8000)