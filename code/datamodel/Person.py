import random
import threading
from time import sleep
import uuid

from code.datamodel import Category


class Person(threading.Thread):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

        self.id = uuid.uuid1()
        self.person_name = ""

        self.longitude = 0
        self.latitude = 0
        self.interests = {}
        self.watch_frequency = 0
        self.variability = 0
        self.friends = []
        self.contents = {}
        self.application = None
        self.estimated_friends = 0

    def add_contacts(self, persons):
        self.estimated_friends = 100 * self.variability
        pers = []
        for person in persons:
            pers.append(person)
        pers.sort(key=lambda per: abs(per.longitude - self.longitude) + abs(per.latitude - self.latitude))
        count = 0
        for per in pers:
            if per is not self:
                if count < self.estimated_friends:
                    self.friends.append(per)
                    count = count + 1


    def set_application(self, application):
        self.application = application

    def run(self):
        while True:
            propositions = self.application.get_propositions()
            chosen = self.choose(propositions)
            self.application.choose(chosen)
            #print 'Time %d %s watch %s' % (self.env.now, str(self), str(chosen))
            yield self.env.timeout(1.0 / self.watch_frequency)

    def choose(self, propositions):
        max_score = 0
        chosen = None
        for k in self.interests:
            move = self.variability * (random.random() - 0.5)*0.1
            friend_move = 0
            for f in self.friends:
                friend_move = friend_move + f.interests[k]
            friend_move = friend_move / max(len(self.friends),1)
            v = self.interests[k] + move + (self.interests[k]-friend_move)*0.1
            if v < 0:
                v = 0
            if v > 1:
                v = 1
            self.interests[k] = v
        for proposition in propositions:
            score = proposition.quality * Category.categories_match(self.interests, proposition.categories) * \
                    (0.5 + random.random())
            if score >= max_score:
                max_score = score
                chosen = proposition
        return chosen

    def __str__(self):
        return "Person => \n    id:         " + str(self.id) + "\n    name:       " + str(self.person_name) \
               + "\n    frequency:  " + str(self.watch_frequency) \
               + "\n    variab:     " + str(self.variability) \
               + "\n    interests:  " + Category.categories_to_str(self.interests) \
               + "\n    friends:    " + str([w.person_name for w in self.friends]) + "\n"

    def __repr__(self):
        return str(self)


