#!/usr/bin/env python
# encoding: utf-8


"""Unit testing helpers."""

import unittest


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant assertion names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue
    assert_in = unittest.TestCase.assertIn

