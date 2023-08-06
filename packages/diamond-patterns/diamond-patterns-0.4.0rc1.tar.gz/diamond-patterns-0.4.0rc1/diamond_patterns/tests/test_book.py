# -*- coding: utf-8 -*-

# from nose.plugins.attrib import attr
from unittest import TestCase
import os


class BookTestCase(TestCase):

    # @attr("single")
    def test_scaffold(self):

        # create temp directory
        directory = "../var/tests/book"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # unpack the pattern with some settings
        os.system("cd ../var/tests/book && ../../../bin/diamond --pattern book noprompt")

        # assert
        assert os.stat("../var/tests/book/Makefile")

        # run the makefile
        os.system("cd ../var/tests/book && make")

        # test for certain files to be built
        assert os.stat("../var/tests/book/.build/mybook.pdf")
