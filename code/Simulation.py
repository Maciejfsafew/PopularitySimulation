#!/usr/bin/python
import simpy

from code.application.Application import Application
from code.generator.PersonGenerator import PersonGenerator


PERSONS = 1000

CONTENTS = 10


def simulation():
    application = Application()
    application.init(CONTENTS)
    env = simpy.Environment()

    generator = PersonGenerator(env)
    persons = []
    for i in xrange(0, PERSONS):
        person = generator.generate_person()
        person.set_application(application)
        persons.append(person)
    for person in persons:
        person.add_contacts(persons)

    env.run(until=100)

    for content in application.contents:
        print content
if __name__ == "__main__":
    simulation()
