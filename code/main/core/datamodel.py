import random
import threading
import uuid

categories = [
    "religion",
    "sport",
    "fashion",
    "science",
    "music",
    "movies",
    "history",
    "money",
    "politics"]


def sort_categories(dictionary):
    pairs = []
    for k, v in dictionary.iteritems():
        pairs.append((k, v))
    pairs.sort(key=lambda pair: -pair[1])
    return pairs


def categories_to_str(dictionary):
    dictionary = sort_categories(dictionary)
    result = "["
    for pair in dictionary:
        result += pair[0] + ": " + str(pair[1]) + " "
    return result + "]"


def categories_match(left, right):
    result = 0
    for key, value in left.iteritems():
        if key in right:
            result += min(value, right[key])
    return result


class Content:
    def __init__(self, name=None, quality=None, categories=None, hits=0):
        self._id = str(uuid.uuid1())
        self.name = name
        self.quality = quality
        self.categories = [] if categories is None else categories
        self.hits = hits

    def __str__(self):
        return "Content => name: " + str(self.name) + " \n    quality: " + str(self.quality) + "  hits: " \
               + str(self.hits) + " categories: " + categories_to_str(self.categories)

    def __repr__(self):
        return str(self)


class Person(threading.Thread):
    def __init__(self, env):
        threading.Thread.__init__(self)
        self.env = env
        if env:
            self.action = env.process(self.run())

        self._id = str(uuid.uuid1())
        self.person_name = ""

        self.longitude = 0
        self.latitude = 0
        self.interests = {}
        self.watch_frequency = 0

        self.friends = []
        self.contents = {}
        self.application = None

    def set_application(self, application):
        self.application = application

    def run(self):
        while True:
            propositions = self.application.get_propositions()
            chosen = self.choose(propositions)
            self.application.choose(chosen)
            print 'Time %d %s watch %s' % (self.env.now, str(self), str(chosen))
            yield self.env.timeout(1.0 / self.watch_frequency)

    def choose(self, propositions):
        max_score = 0
        chosen = None
        for proposition in propositions:
            score = proposition.quality * categories_match(self.interests, proposition.categories) * \
                    (0.5 + random.random())
            if score > max_score:
                max_score = score
                chosen = proposition
        return chosen

    def __str__(self):
        return "Person => \n    id:         " + str(self._id) + "\n    name:       " + str(self.person_name) \
               + "\n    frequency:  " + \
               str(self.watch_frequency) + "\n    interests:  " + categories_to_str(self.interests) + "\n"

    def __repr__(self):
        return str(self)


class Hit(object):
    def __init__(self, who, what, when):
        self._id = str(uuid.uuid1())
        self.who = who
        self.what = what
        self.when = when

    pass