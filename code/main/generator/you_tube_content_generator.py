import random
import re
import urllib2
import sys
import math

from bs4 import BeautifulSoup

from code.main.core import datamodel
from code.main.core.dao import ContentDao


__author__ = 'mjjaniec'

div_style = "yt-lockup-content"
title_style = "yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"
title_attribute = "title"
url = "https://www.youtube.com/results?search_query="

max_hits = 10000000000
dao = ContentDao()


def generate_categories(hints):
    interests = []
    sum = 0.0
    if len(hints) == 1:
        hint_space = 0.5 + random.random() / 2
    else:
        hint_space = 0.75 + random.random() / 4

    rest_space = 1.0 - hint_space
    for i in xrange(random.randint(0, 4 - len(hints))):
        val = random.expovariate(1)
        interests.append(val)
        sum += val
    interests = map(lambda x: rest_space * x / sum, interests)

    result = {}
    if len(hints) == 1:
        result[hints[0]] = hint_space
    else:
        ratio = 2 + 2 * random.random()
        result[hints[0]] = hint_space * ratio / (ratio + 1)
        result[hints[1]] = hint_space * 1 / (ratio + 1)

    if len(interests) > 0:
        for val in interests:
            category = None
            while True:
                category = random.choice(datamodel.categories)
                if not category in result:
                    break
            result[category] = val
    else:
        result[hints] = 1.0
    return result


def print_menu():
    count = dao.find_all().count()
    print "\n\nThere is {0} entries in database. ".format(count)
    print "   [1] import dumped data"
    print "   [2] download data from YouTube"
    print "   [3] dump data"
    print "   [0] exit"


def select_categories():
    print "select primary category:"
    i = 0
    for cat in datamodel.categories:
        print "[" + str(i) + "] " + cat
        i += 1
    primary_category = datamodel.categories[int(sys.stdin.readline())]

    print "select secondary category:"
    i = 0
    for cat in datamodel.categories:
        print "[" + str(i) + "] " + cat
        i += 1
    print "[" + str(i) + "] None"
    choice = int(sys.stdin.readline())

    if choice >= len(datamodel.categories):
        return [primary_category]
    else:
        return [primary_category, datamodel.categories[choice]]


def download():
    categories = select_categories()
    if len(categories) == 1:
        print "enter search query for category: " + categories[0]
    else:
        print "enter search query for categories: " + categories[0] + " " + categories[1]
    query = sys.stdin.readline()

    print "downloading data..."
    response = urllib2.urlopen(url + re.sub(" ", "+", query))
    html = response.read()
    soup = BeautifulSoup(html)
    contents = []

    for tag in soup.find_all("div", class_=div_style):
        try:
            title = tag.find_all("a", class_=title_style)
            title = title[0][title_attribute]
            title = title.encode('ascii', errors='ignore')

            hits = tag.find_all("li")
            hits = "".join(re.findall(r"\d+", hits[2].text))
            hits = float(hits)

            quality = math.log(hits) / math.log(max_hits)

            content = datamodel.Content(title, quality, generate_categories(categories))
            contents.append(content)
        except:
            pass

    for content in contents:
        print content

    print "\n\n Is this data good?"
    print "   [1] Yes, please store it in database"
    print "   [2] No, drop it"

    choice = int(sys.stdin.readline())
    if choice == 1:
        for content in contents:
            dao.put(content)
        print "data stored in db"
    else:
        print "data dropped"


def main():
    while True:
        print_menu()
        choice = int(sys.stdin.readline())
        if choice == 0:
            break
        if choice == 1:
            dao.import_data(dao.collection_name + ".json")
        if choice == 2:
            download()
        if choice == 3:
            dao.export_data(dao.collection_name + ".json")


if __name__ == "__main__":
    main()

