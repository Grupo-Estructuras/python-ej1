import re
import json
import threading
import requests
import common.exceptions
from asyncio import exceptions
from bs4 import BeautifulSoup


def scrapeGithub(languages, config, resultfile):
    langList = []
    min = 0
    max = 0

    aliases = config["aliases"]
    with open(resultfile, "w") as resultsFile:
        gitpages = []
        threads = []
        for language in languages:
            try:
                langAlias = aliases[language]
            except KeyError:
                langAlias = language

            link = str.format(config["github_site_format"], langAlias)
            print(link)

            sem = threading.Semaphore(config["max_parallel"])
            threads.append(threading.Thread(
                target=language_read, args=(link, gitpages, sem, language)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for gitpage in gitpages:
            if gitpage[0].status_code != 200:
                print(gitpage[0].status_code)
                raise common.exceptions.RequestException()

            githubsoup = BeautifulSoup(
                gitpage[0].text, features="html.parser")
            gitLenCant = githubsoup.find(class_="h3 color-fg-muted").text
            gitLenCant = re.search("\d+(,\d*)*", gitLenCant).group()
            gitLenCant = int(gitLenCant.replace(",", ""))

            min = min if min < gitLenCant and min != 0 else gitLenCant
            max = max if max > gitLenCant else gitLenCant

            langItem = {
                "name": gitpage[1],
                "repoAmmount": gitLenCant,
                "rating": 0
            }

            resultsFile.write(
                langItem["name"] + "," + str(langItem["repoAmmount"]) + "\n")
            langList.append(langItem)

    return ratingSorter(min, max, langList)


def language_read(link, pages, sem, language):
    sem.acquire()
    pages.append((requests.get(link), language))
    sem.release()


# Adds rating to each item and returns the list sorted by rating
def ratingSorter(min, max, list):
    for item in list:
        item["rating"] = (item["repoAmmount"] - min) / (max - min) * 100

    return sorted(list, key=lambda i: i["rating"], reverse=True)
