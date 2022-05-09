from common.configuration import configure
from scraping.githubscraper import scrapeInterest
from graph.barChart import graphInterest
from common import exceptions


def main():
    config = configure()

    topics = scrapeInterest(config["scraper"])
    for topic in topics:
        print(f"{topic[0]}:{topic[1]}")
    graphInterest(topics)


main()
