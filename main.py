import requests
from bs4 import BeautifulSoup
import csv


def scrapeMercadolibre(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")
    casas = soup.find_all("div", class_="ui-search-result__wrapper")
    
    # Crear una lista de diccionarios para representar las casas.
    resultados = []
    
    for casa in casas:

        # agarro la cantidad de banos
        ul = casa.find("ul", class_="ui-search-card-attributes ui-search-item__attributes-grid")
        info_casa = ul.find_all("li")

        #Obtener la localidad de las casas
        localidad = casa.find("span", class_="ui-search-item__location-label")
        
        if len(info_casa) == 3:
            resultados.append({
            "titulo": casa.find("h2", class_="ui-search-item__title").text,
            "precio": (casa.find("span", class_="andes-money-amount__fraction").text).replace(".",""),
            "ambientes": info_casa[0].text,
            "baños": info_casa[1].text,
            "superficie":info_casa[2].text,
            "localidad": localidad.text
            })
        else:
            resultados.append({
                "titulo": casa.find("h2", class_="ui-search-item__title").text,
                "precio": (casa.find("span", class_="andes-money-amount__fraction").text).replace(".",""),
            })

    return resultados

def writeCsv(results):
    '''
        result = {
            'titulo' : 'casa etc etc',
            'precio' : '1902',
            'superficie':'32m2'
            'banos':'3'
            'dormitorios':'3',
        }
    '''
    nombre_archivo = "casasMercadoLibre.csv"
    
    with open(nombre_archivo, 'a', newline='') as archivo_csv:
        # Crear un objeto escritor CSV
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=['titulo', 'precio','ambientes', 'baños', 'superficie', 'localidad'])

        # Escribir los datos de cada objeto en el array
        for resultado in results:
            escritor_csv.writerow(resultado)

if __name__ == "__main__":

    url = "https://listado.mercadolibre.com.ar/casas#D[A:casas]"
    r = requests.get(url)

    nombre_archivo = "casasMercadoLibre.csv"
    
    # escribimos los csv primero antes de llenar los campos
    with open(nombre_archivo, 'w', newline='') as outcsv:
        writer = csv.DictWriter(outcsv,  fieldnames=['titulo', 'precio','ambientes', 'baños', 'superficie', 'localidad'])
        writer.writeheader()
    
    # Guardar los datos de todas las paginas
    while url:

        resultados = scrapeMercadolibre(url)
        writeCsv(resultados)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        
        li = soup.find("li", class_="andes-pagination__button andes-pagination__button--next")
        next_url = li.find("a", class_="andes-pagination__link ui-search-link")
        
        url = next_url.get("href")
        

class Casa(object):
    def __init__(self, titulo, precio, ambientes, banos, superficie, localidad):
        self.titulo = titulo
        self.precio = precio
        self.ambientes = ambientes
        self.banos = banos
        self.superficie = superficie
        self.localidad = localidad