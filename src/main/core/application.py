import random

from src.main.core.dao import HitDao
from src.main.core.datamodel import Hit


__author__ = 'mjjaniec'


class Application(object):
    def __init__(self):
        self.contents = {}
        self.all_hits = 0
        self.hits_dao = HitDao()

    def init(self, contents):
        self.contents = {content: 0 for content in contents}

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

    def choose(self, user, chosen_content, when):
        chosen_content.hits += 1
        #should use ID, but who cares
        self.hits_dao.put(Hit(user.person_name, chosen_content.name, when))
        self.all_hits += 1
        self.contents[chosen_content] += 1

