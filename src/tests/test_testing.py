#!/usr/bin/env python
# encoding: utf-8


"""Unit testing and example usage of the Pep8TestCase"""

import unittest
from craigs_python_utils.testing import Pep8TestCase


class Pep8CompliantMethodNamesExposed(Pep8TestCase):
    """Ensure expected methods are available."""

    def test_it_should_expose_assert_equal(self):
        self.assert_equal(10, 10)

    def test_it_should_expose_assert_in(self):
        self.assert_in("foo", ["bar", "foo", "baz"])

    def test_it_should_expose_assert_raises(self):
        def always_raise():
            raise Exception()
        self.assert_raises(Exception, always_raise)

    def test_it_should_expose_assert_true(self):
        self.assert_true(True)


if __name__ == '__main__':
    unittest.main()

