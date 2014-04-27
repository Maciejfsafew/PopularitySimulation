import random

from code.generator.ContentGenerator import ContentGenerator


__author__ = 'mjjaniec'


class Application(object):
    def init(self, number_of_contents):
        self.contents = {self.generator.generate_content(): 0 for i in xrange(number_of_contents)}

    def __init__(self):
        self.contents = {}
        self.all_hits = 0
        self.generator = ContentGenerator()

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

