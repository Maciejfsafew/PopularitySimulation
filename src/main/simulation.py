#!/usr/bin/python
import simpy

from src.main.core.application import Application
from src.main.core.dao import ensure_valid_database_state, PersonDao, ContentDao

PERSONS = 10
CONTENTS = 10


def simulation():
    ensure_valid_database_state()
    application = Application()
    env = simpy.Environment()

    content_dao = ContentDao()
    person_dao = PersonDao()
    contents = [content for content in content_dao.find().limit(CONTENTS)]
    persons = [person.init(env, application) for person in person_dao.find().limit(PERSONS)]

    application.init(contents)
    print "starting simulation..."
    env.run(until=100)

    print "saving results..."

    for content in contents:
        content_dao.put(content)

    for person in persons:
        person_dao.put(person)

    print "done"


if __name__ == "__main__":
    simulation()
