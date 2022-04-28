import requests
from bs4 import BeautifulSoup

import common.exceptions

def scrapeTiobe():
    tiobePage = requests.get("https://www.tiobe.com/tiobe-index/")
    if tiobePage.status_code != 200:
        raise common.exceptions.RequestException()
    
    tiobesoup = BeautifulSoup(tiobePage.text, features="html.parser")

    top20_elem = tiobesoup.find_all(class_="td-top20")

    if len(top20_elem) < 20:
        print("Aviso: No se encontraron 20 entradas en tiobe. Tratando seguir igual...")
    

    return [language.find_next("td").text for language in top20_elem]
