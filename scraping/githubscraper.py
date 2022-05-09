import re
import json
import requests
import common.exceptions
from asyncio import exceptions
from bs4 import BeautifulSoup


def scrapeGithub(languages):
    langList = []
    min = 0
    max = 0

    with open("./data/langAliases.json") as jsonFile:
        with open("./data/Resultados.txt", "w") as resultsFile:
            aliases = json.load(jsonFile)

            for language in languages:
                try:
                    langAlias = aliases[language.lower()]
                except KeyError:
                    langAlias = language

                link = f"https://github.com/topics/{langAlias}"
                gitpage = requests.get(link)

                if gitpage.status_code != 200:
                    raise common.exceptions.RequestException()

                githubsoup = BeautifulSoup(
                    gitpage.text, features="html.parser")
                gitLenCant = githubsoup.find(class_="h3 color-fg-muted").text
                gitLenCant = re.search("\d+(,\d*)*", gitLenCant).group()
                gitLenCant = int(gitLenCant.replace(",", ""))

                min = min if min < gitLenCant and min != 0 else gitLenCant
                max = max if max > gitLenCant else gitLenCant

                langItem = {
                    "name": language,
                    "repoAmmount": gitLenCant,
                    "rating": 0
                }

                resultsFile.write(
                    langItem["name"] + "," + str(langItem["repoAmmount"]) + "\n")
                langList.append(langItem)
                print(f"Reading...{language}")

    return ratingSorter(min, max, langList)


# Adds rating to each item and returns the list sorted by rating
def ratingSorter(min, max, list):
    for item in list:
        item["rating"] = (item["repoAmmount"] - min) / (max - min) * 100

    return sorted(list, key=lambda i: i["rating"], reverse=True)
