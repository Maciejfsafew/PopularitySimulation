__author__ = 'Maciej'

import simpy

USERS = 100
persons = []


class Person(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
        self.delay = 10


    def run(self):
        while True:
            print('Time %d ' % env.now )

            yield self.env.timeout(self.delay)


if __name__ == "__main__":
    env = simpy.Environment()
    for i in xrange(0, USERS):
        persons.append(Person(env))

    env.run(until=100)