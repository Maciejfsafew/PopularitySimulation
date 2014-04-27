__author__ = 'mjjaniec'

Category = [
    "religion",
    "sport",
    "fashion",
    "science",
    "music",
    "movies",
    "history",
    "money",
    "politics"]


def sort_categories(dictionary):
    pairs = []
    for k, v in dictionary.iteritems():
        pairs.append((k, v))
    pairs.sort(key=lambda pair: -pair[1])
    return pairs


def categories_to_str(dictionary):
    dictionary = sort_categories(dictionary)
    result = "["
    for pair in dictionary:
        result += pair[0] + ": " + str(pair[1]) + " "
    return result + "]"


def categories_match(left, right):
    result = 0
    for key, value in left.iteritems():
        if key in right:
            result += min(value, right[key])
    return result