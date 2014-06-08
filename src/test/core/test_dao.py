import unittest

from src.main.core.dao import ContentDao
from src.main.core.datamodel import Content, categories


__author__ = 'mjjaniec'


class TestContentDao(unittest.TestCase):
    def setUp(self):
        self.dao = ContentDao(use_test=True)

    def test_one(self):
        x = Content("13")
        self.dao.put(x),
        self.assertGreater(self.dao.find().count(), 0)
        self.dao.remove_all()
        self.assertEqual(self.dao.find().count(), 0)

    def test_dao(self):
        self.dao.remove_all()
        c1 = Content(name="ala", quality=0.2, categories={categories[1]: 0.8, categories[4]: 0.2})
        self.dao.put(c1)
        results = self.dao.find({"_id": "ala"})
        self.assertEqual(results.count(), 1)
        c2 = results.next()
        self.assertTrue(isinstance(c2, Content))
        self.assertDictEqual(c1.__dict__, c2.__dict__)
