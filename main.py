import argparse
from distutils.command.config import config
import json
import logging
from zipfile import _ReadWriteMode
from yaml import parse
from scraping.tiobescraper import scrapeTiobe
from scraping.githubscraper import scrapeGithub
from graph.barChart import createBarChart
from common import exceptions


def configure():
    # Crear configuración por defecto en caso de que no existe un archivo
    defconfig = {
        "usar_lista_fija": False,
        "lista_lenguajes": [],
        "scraper": {
            "tiobe_site_format": "https://www.tiobe.com/tiobe-index/",
            "github_site_format": "https://github.com/topics/{}",
            "aliases": {
                "C#": "csharp",
                "C++": "cpp",
                "Classic Visual Basic": "visual-basic",
                "Delphi/Object Pascal": "delphi"
            },
            "retry_delays_ms": [
                300,
                600,
                1200,
            ],
            "max_pages_interest": 10,
            "interest": "sort",
            "max_parallel": 5,
            "github_interest_format": "https://github.com/topics/{}?o=desc&s=updated&page={}"
        },
        "archivo_resultado": "data/Resultados.txt"
    }

    # Leer argumentos para ver que archivo de configuración usar
    parser = argparse.ArgumentParser(description="Parsear Github")
    parser.add_argument("-c", "--config", type=str, default="data/config.json")
    args = parser.parse_args()

    # Intentar abrir
    try:
        with open(args.config, "r+") as configfile:
            # Cargar valores que se encuentran en archivo
            defconfig.update(json.load(configfile))

            # Volver a escribir (en caso de que alguna información no se encontraba inicialmente en el archivo)
            configfile.seek(0)
            json.dump(defconfig, configfile)
            configfile.truncate()
    except IOError:
        logging.warning(
            "No se pudo abrir archivo. Usando configuración predeterminada...")

    return defconfig


def main():
    config = configure()

    languages = []
    if not config.usar_lista_fija:
        try:
            languages = scrapeTiobe()
        except exceptions.RequestException as err:
            logging.error(
                f"No se pudo conectar con la página tiobe. Verifique su conexión. Error: {err}")
            return -1
    else:
        languages = config.lista_lenguajes

    try:
        langDataArr = scrapeGithub(languages, config.scraper)
    except exceptions.RequestException as err:
        logging.error(
            f"No se pudo conectar con la página github. Verifique su conexión. Error: {err}")
        return -1

    position = 0
    for language in langDataArr:
        position += 1
        print(
            f"{str(position)} - {language['name']},{language['rating']},{language['repoAmmount']}")

    createBarChart(langDataArr)


main()
