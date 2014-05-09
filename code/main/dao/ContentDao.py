from code.main.dao.BaseDao import BaseDao
from code.main.datamodel import Content

__author__ = 'mjjaniec'


class ContentDao(BaseDao):
    collection_name = "contents"

    def __init__(self, use_test=False):
        BaseDao.__init__(self, Content, ContentDao.collection_name, use_test)


