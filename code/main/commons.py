import os

__author__ = 'mjjaniec'


def get_resource_path(resource_name):
    """ returns path to file placed in "resources" directory  """
    directory = "."
    for i in xrange(5):
        for name in os.listdir(directory):
            if name == "resources":
                return directory + "/resources/" + resource_name
        directory += "/.."