__author__ = 'mjjaniec'


class Hit(object):
    def __init__(self, person_id, content_id, datetime):
        self.person_id = person_id
        self.content_id = content_id
        self.datetime = datetime