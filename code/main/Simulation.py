#!/usr/bin/python
import simpy

from code.main.dao.PersonDao import PersonDao
from code.main.generator import PersonGenerator


PERSONS = 1

CONTENTS = 10


def ensure_valid_database_state(clear_database):
    person_dao = PersonDao();
    content_dao = ContentDao();
    h
    if clear_database


def simulation():
    ensure_valid_database_state()
    application = application()
    application.init(CONTENTS)
    env = simpy.Environment()

    generator = PersonGenerator(env)
    for i in xrange(0, PERSONS):
        person = generator.generate_person()
        person.set_application(application)

    env.run(until=100)


if __name__ == "__main__":
    simulation()
