from flask import Flask, Response 
import csv
import json

app = Flask(__name__)

directory = "casasMercadoLibre.csv"

# read data from csv file
def ReadData():
    dataJson = [] 
    with open(directory, "r") as file:
        fileReader = csv.DictReader(file)
        
        for row in fileReader:
            data = {}
            data['titulo'] = row['titulo']
            data['precio'] = row['precio']
            data['ambientes'] = row['ambientes']
            data['banos'] = row['baños']
            data['superficie'] = row['superficie']
            data['localidad'] = row['localidad']
            
            dataJson.append(data)
    
    return dataJson

data = ReadData()
print(data)

# Da como respuesta todas las propiedades
@app.route("/alldata")
def getData():
    return Response(json.dumps(data[:3]), mimetype="application/json")

# filtra las propiedades por localidad
@app.route("/data/localidad/<localidad>")
def GetForlocalidad(localidad): 
    localidadData = []
    
    for loc in data:
        if localidad.lower() in loc['localidad'].lower():
            localidadData.append(loc)
    
    if len(localidadData) != 0:
        return Response(json.dumps(localidadData), mimetype="application/json")
    else:
        return "<p>No se encontraron resultados</p>"

@app.route("/data/price/<price>") 
def GetForPrice(price):
    priceData = []

    for p in data:
        if price == p['precio']:
            priceData.append(p)

    if len(priceData) != 0:
        return Response(json.dumps(priceData), mimetype="application/json")
    else:
        return "<p>No se encontraron resultados</p>"
    

@app.route("/data/bathroom/<bathroom>") 
def GetForBathroom(bathroom):
    bathData = []

    for p in data:
        if bathroom in p['banos']:
            bathData.append(p)

    if len(bathData) != 0:
        return Response(json.dumps(bathData), mimetype="application/json")
    else:
        return "<p>No se encontraron resultados</p>"
