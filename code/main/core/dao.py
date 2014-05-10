import os
import subprocess
import new

import pymongo

from code.main.core.datamodel import Content, Person, Hit

from code.main.generator.person_generator import PersonGenerator


__author__ = 'mjjaniec'


class BaseDao(object):
    database_address = "mongodb://localhost:27017/"
    test_database = "miss_test"
    main_database = "miss_main"
    connection = pymongo.MongoClient(database_address)

    def __init__(self, clazz, collection_name, use_test):
        if use_test:
            self.database = BaseDao.connection[BaseDao.test_database]
        else:
            self.database = BaseDao.connection[BaseDao.main_database]
        self.collection = self.database[collection_name]
        self.clazz = clazz

    def export_data(self, file_name):
        subprocess.call(["mongoexport",
                         "--db", self.database.name,
                         "--collection", self.collection.name,
                         "--out", BaseDao.find_resources() + file_name])

    def import_data(self, file_name):
        self.remove_all()
        subprocess.call(["mongoimport",
                         "--db", self.database.name,
                         "--collection", self.collection.name,
                         "--file", BaseDao.find_resources() + file_name])

    def remove_all(self):
        self.collection.remove()

    def find_all(self):
        return self.collection.find()

    def put(self, entry):
        self.collection.update({"_id": entry._id}, entry.__dict__, upsert=True)

    def find(self, query=None):
        cursor = self.collection.find(query)
        clazz = self.clazz

        def new_next(cursors_self):
            raw = cursors_self._old_next()
            result = new.instance(clazz)
            result.__dict__ = raw
            return result

        cursor._old_next = cursor.next
        cursor.next = new.instancemethod(new_next, cursor)
        return cursor

    @staticmethod
    def find_resources():
        directory = "."
        for i in xrange(5):
            for name in os.listdir(directory):
                if name == "resources":
                    return directory + "/resources/"
            directory += "/.."


class ContentDao(BaseDao):
    collection_name = "contents"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Content, ContentDao.collection_name, use_test)


class PersonDao(BaseDao):
    collection_name = "persons"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Person, PersonDao.collection_name, use_test)


class HitDao(BaseDao):
    collection_name = "hits"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Hit, HitDao.collection_name, use_test)


def ensure_valid_database_state(clear_database=True, min_persons=100, min_content=100):
    content_dao = ContentDao()
    person_dao = PersonDao()
    hit_dao = HitDao()

    if clear_database:
        content_dao.remove_all()
        person_dao.remove_all()
        hit_dao.remove_all()

    persons_count = person_dao.find_all().count()
    if persons_count < min_persons:
        person_gen = PersonGenerator(None)
        while persons_count < min_persons:
            person_dao.put(person_gen.generate_person())
            persons_count += 1

    if content_dao.find_all().count() < min_content:
        content_dao.import_data("contents.json")
    if content_dao.find_all().count() < min_content:
        print "not enough data gathered, use you_tube_content_generator to generate new content"
        exit(0)