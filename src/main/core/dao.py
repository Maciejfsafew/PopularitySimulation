import subprocess
import new

import pymongo
from pymongo.cursor import Cursor

from src.main import commons
from src.main.core.datamodel import Content, Person, Hit
from src.main.generator.person_generator import PersonGenerator


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
                         "--out", commons.get_resource_path(file_name)])

    def import_data(self, file_name):
        self.remove_all()
        subprocess.call(["mongoimport",
                         "--db", self.database.name,
                         "--collection", self.collection.name,
                         "--file", commons.get_resource_path(file_name)])

    def remove_all(self):
        self.collection.remove()

    def put(self, entry):
        self.collection.update({"_id": entry._id}, entry.__dict__, upsert=True)

    def find(self, query=None):
        class SmartCursor(Cursor):
            def __init__(self, ordinary_cursor, clazz):
                self.__dict__ = ordinary_cursor.__dict__
                self.clazz = clazz
                self.ordinary_cursor = ordinary_cursor

            def next(self):
                raw = self.ordinary_cursor.next()
                result = new.instance(self.clazz)
                result.__dict__ = raw
                return result

        return SmartCursor(self.collection.find(query), self.clazz)


class ContentDao(BaseDao):
    collection_name = "contents"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Content, ContentDao.collection_name, use_test)


class PersonDao(BaseDao):
    collection_name = "persons"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Person, PersonDao.collection_name, use_test)

    #Override
    def put(self, entry):
        friends = [friend.person_name for friend in entry.friends]
        dictionary = {
            "_id": entry._id,
            "person_name": entry.person_name,
            "interests": entry.interests,
            "watch_frequency": entry.watch_frequency,
            "hits": entry.hits,
            "longitude": entry.longitude,
            "latitude": entry.latitude,
            "friends": friends,
            "variability": entry.variability
        }
        self.collection.update({"_id": entry._id}, dictionary, upsert=True)


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

    persons_count = person_dao.find().count()
    if persons_count < min_persons:
        person_gen = PersonGenerator(None)
        while persons_count < min_persons:
            person_dao.put(person_gen.generate_person())
            persons_count += 1

    if content_dao.find().count() < min_content:
        content_dao.import_data("contents.json")
    if content_dao.find().count() < min_content:
        print "not enough data gathered, use you_tube_content_generator to generate new content"
        exit(0)