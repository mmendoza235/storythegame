from nose.tools import *
import inspect
import os
import storythegame.stg


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_basic():
    print "I RAN!"
