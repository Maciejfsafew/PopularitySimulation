#!/usr/bin/python
from code.application.Application import Application
from code.generator.PersonGenerator import PersonGenerator


PERSONS = 1

CONTENTS = 10


def simulation():
    application = Application()
    application.init(CONTENTS)

    generator = PersonGenerator()
    for i in xrange(0, PERSONS):
        person = generator.generate_person()
        person.set_application(application)
        person.start()


if __name__ == "__main__":
    simulation()
