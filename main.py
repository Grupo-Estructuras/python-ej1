from common import exceptions
import requests
import re
from bs4 import BeautifulSoup
from scraping import tiobescraper

def main():
    try:
        list = tiobescraper.scrapeTiobe()
    except exceptions.RequestException as err:
        print("No se pudo conectar con la página tiobe. Verifique su conexión. Error: "+err)
        return -1

    
    print(list)
    languages=list
    for language in languages:
        link="https://github.com/topics/"+language
        gitpage=requests.get(link)
        githubsoup = BeautifulSoup(gitpage.text, features="html.parser")
        gitLenCant = githubsoup.find(class_="h3 color-fg-muted").text
        
        gitLenCant = re.search("\d+(,\d*)*",gitLenCant).group()
        gitLenCant = language + " = " + gitLenCant
        print (gitLenCant)

main()
