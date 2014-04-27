import random
import threading
from time import sleep
import uuid

from code.datamodel import Category


class Person(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.id = uuid.uuid1()
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
            sleep(random.expovariate(1.0 / self.watch_frequency))
            propositions = self.application.get_propositions()
            chosen = self.choose(propositions)
            self.application.choose(chosen)
            print str(self) + " watch " + str(chosen)

    def choose(self, propositions):
        max_score = 0
        chosen = None
        for proposition in propositions:
            score = proposition.quality * Category.categories_match(self.interests, proposition.categories) * \
                    (0.5 + random.random())
            if score > max_score:
                max_score = score
                chosen = proposition
        return chosen

    def __str__(self):
        return "Person => \n    id:         " + str(self.id) + "\n    name:       " + str(self.person_name) \
               + "\n    frequency:  " + \
               str(self.watch_frequency) + "\n    interests:  " + Category.categories_to_str(self.interests) + "\n"

    def __repr__(self):
        return str(self)


