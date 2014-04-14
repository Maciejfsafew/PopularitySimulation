#!/usr/bin/python

from datamodel.Person import Person
from datamodel.Website import Website

PERSONS = 1000

WEBSITES = 1000


def simulation():
  
  participants = []
  for i in xrange(0,PERSONS):
    participants.append(Person())

  for i in xrange(0,WEBSITES):
    participants.append(Website())


if __name__ == "main":
  simulation()
