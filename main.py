from scraping.tiobescraper import scrapeTiobe
from scraping.githubscraper import scrapeGithub
from graph.barChart import createBarChart
from common import exceptions


def main():
    try:
        languages = scrapeTiobe()
    except exceptions.RequestException as err:
        print(f"No se pudo conectar con la página tiobe. Verifique su conexión. Error: {err}")
        return -1

    try:
        langDataArr = scrapeGithub(languages)
    except exceptions.RequestException as err:
        print(f"No se pudo conectar con la página github. Verifique su conexión. Error: {err}")
        return -1

    position = 0
    for language in langDataArr:
        position += 1
        print(f"{str(position)} - {language['name']},{language['rating']},{language['repoAmmount']}")

    createBarChart(langDataArr)

main()
