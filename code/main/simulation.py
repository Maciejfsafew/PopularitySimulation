#!/usr/bin/python
import simpy

from code.main.core.application import Application
from code.main.core.dao import ensure_valid_database_state
from code.main.generator.person_generator import PersonGenerator

PERSONS = 1

CONTENTS = 10


def simulation():
    ensure_valid_database_state()
    application = Application()
    application.init(CONTENTS)
    env = simpy.Environment()

    generator = PersonGenerator(env)
    for i in xrange(0, PERSONS):
        person = generator.generate_person()
        person.set_application(application)

    env.run(until=100)


if __name__ == "__main__":
    pass
