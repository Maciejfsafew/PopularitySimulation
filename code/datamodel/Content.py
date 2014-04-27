import uuid

import Category


class Content:
    def __init__(self, name=None, quality=None, categories=None):
        self.id = uuid.uuid1()
        self.name = name
        self.quality = quality
        self.categories = categories
        self.hits = 0

    def __str__(self):
        return "Content => \n    id:         " + str(self.id) + "\n    name:      " \
               + str(self.name) + "\n    quality:    " + str(self.quality) + "\n    hits:       " + str(self.hits) \
               + "\n    categories: " + Category.categories_to_str(self.categories) + "\n"

    def __repr__(self):
        return str(self)
