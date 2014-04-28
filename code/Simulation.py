#!/usr/bin/python
import simpy

from code.application.Application import Application
from code.generator.PersonGenerator import PersonGenerator


PERSONS = 1

CONTENTS = 10


def simulation():
    application = Application()
    application.init(CONTENTS)
    env = simpy.Environment()

    generator = PersonGenerator(env)
    for i in xrange(0, PERSONS):
        person = generator.generate_person()
        person.set_application(application)

    env.run(until=100)


if __name__ == "__main__":
    simulation()
