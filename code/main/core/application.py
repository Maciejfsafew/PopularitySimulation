import random

from code.main.core.dao import ContentDao


__author__ = 'mjjaniec'


class Application(object):
    def init(self, number_of_contents):
        self.contents = []
        cursor = ContentDao().find_all()
        while True:
            content = cursor.next()
            if content is None:
                break
            self.contents.append(content)

    def __init__(self):
        self.contents = {}
        self.all_hits = 0

    def get_propositions(self):
        result = []
        for i in xrange(6):
            while True:
                content = random.choice(self.contents.keys())
                if content in result:
                    continue
                    #  estimate = float((self.contents[content] + 1) / (self.all_hits + 1)) / math.sqrt(len(self.contents))
                    # if estimate > random.random():
                result.append(content)
                break
        return result

    def choose(self, chosen_content):
        chosen_content.hits += 1
        self.all_hits += 1
        self.contents[chosen_content] += 1

