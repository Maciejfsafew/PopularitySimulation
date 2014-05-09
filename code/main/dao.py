__author__ = 'mjjaniec'

import new

import pymongo


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
