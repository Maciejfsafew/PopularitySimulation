import re
import urllib2
import sys
import math

from bs4 import BeautifulSoup

from code.main.datamodel import Category


__author__ = 'mjjaniec'

div_style = "yt-lockup-content"
title_style = "yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"
title_attribute = "title"
url = "https://www.youtube.com/results?search_query="

max_hits = 10000000000


def main():
    while True:
        print "select category"
        i = 0
        for cat in Category.Category:
            print "[" + str(i) + "] " + cat
            i += 1
        category = Category.Category[int(sys.stdin.readline())]
        print "enter search query for category: " + category
        keyword = sys.stdin.readline()

        response = urllib2.urlopen(url + re.sub(" ", "+", keyword))
        html = response.read()
        soup = BeautifulSoup(html)
        for tag in soup.find_all("div", class_=div_style):
            try:
                title = tag.find_all("a", class_=title_style)
                title = title[0][title_attribute]
                title = '""" ' + title + ' """'

                hits = tag.find_all("li")
                hits = "".join(re.findall(r"\d+", hits[2].text))
                hits = float(hits)

                quality = math.log(hits) / math.log(max_hits)

                print 'Content(' + title + ", " + str(quality) + \
                      ", ContentGenerator._generate_categories(\"" + category + "\")),"
            except:
                pass


if __name__ == "__main__":
    main()
