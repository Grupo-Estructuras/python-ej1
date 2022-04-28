import imp
from common import exceptions
from scraping import tiobescraper

def main():
    try:
        list = tiobescraper.scrapeTiobe()
    except exceptions.RequestException as err:
        print("No se pudo conectar con la página tiobe. Verifique su conexión. Error: "+err)
        return -1

    
    print(list)


main()
