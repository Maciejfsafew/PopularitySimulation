import random
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


class Person:
    def __init__(self):
        self._id = str(uuid.uuid1())
        self.person_name = ""

        self.variability = 0
        self.longitude = 0
        self.latitude = 0
        self.interests = {}
        self.watch_frequency = 0
        self.hits = 0

        self.friends = []
        self.contents = {}
        self.env = None
        self.action = None
        self.application = None
        self.variability = 0

    def init(self, env, application):
        self.contents = {}
        self.env = env
        self.application = application
        self.action = env.process(self.run())
        return self

    def add_contacts(self, persons):
        estimated_friends = 20 * self.variability
        pers = []
        for person in persons:
            pers.append(person)
        pers.sort(key=lambda per: abs(per.longitude - self.longitude) + abs(per.latitude - self.latitude))
        count = 0
        for per in pers:
            if per is not self:
                if count < estimated_friends:
                    self.friends.append(per)
                    count += 1

    def run(self):
        while True:
            propositions = self.application.get_propositions()
            chosen = self.choose(propositions)
            self.hits += 1
            self.application.choose(self, chosen, self.env.now)
            if not chosen in self.contents:
                self.contents[chosen] = 1
            else:
                self.contents[chosen] += 1
            yield self.env.timeout(1.0 / self.watch_frequency)

    def choose(self, propositions):
        max_score = -100.0
        chosen = None

        tmp_interests = {}
        for k in self.interests:
            move = self.variability * (random.random() - 0.5) * 0.1
            friend_move = 0
            for f in self.friends:
                friend_move = friend_move + f.interests[k]
            friend_move = friend_move / max(len(self.friends), 1)
            v = self.interests[k] + move + (self.interests[k] - friend_move) * 0.1
            if v < 0:
                v = 0
            if v > 1:
                v = 1
            tmp_interests[k] = v
        for proposition in propositions:
            score = proposition.quality * categories_match(tmp_interests, proposition.categories) * \
                    (0.5 + random.random())
            if proposition in self.contents:
                score /= self.contents[proposition]
            if score >= max_score:
                max_score = score
                chosen = proposition
        return chosen

    def __str__(self):
        return "Person => \n    id:         " + str(self._id) + "\n    name:       " + str(self.person_name) \
               + "\n    frequency:  " + \
               str(self.watch_frequency) + "\n    interests:  " + categories_to_str(self.interests) + "\n"

    def __repr__(self):
        return str(self)


class Hit:
    def __init__(self, who, what, when):
        self._id = str(uuid.uuid1())
        self.who = who
        self.what = what
        self.when = when

    pass