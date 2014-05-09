from code.main.dao.BaseDao import BaseDao
from code.main.datamodel.Person import Person

__author__ = 'mjjaniec'


class PersonDao(BaseDao):
    collection_name = "persons"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Person, PersonDao.collection_name, use_test)


