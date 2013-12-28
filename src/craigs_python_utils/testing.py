#!/usr/bin/env python
# encoding: utf-8


"""Unit testing helpers."""

import unittest
import platform
import re
from os.path import exists, isfile, isdir, islink
from craigs_python_utils.os_cmds import _sudo


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant assertion names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue
    assert_in = unittest.TestCase.assertIn


class FileSystemAssertsMixin(object):
    "Mix this class into your TestCase to get some file system assertions"

    def assert_file_exists(self, filepath, kind="any"):
        "Check if filepath exists and is a <file|dir|link>"

        self.assert_true(exists(filepath))

        if "file" in kind.lower():
            self.assert_true(isfile(filepath))
        elif "dir" in kind.lower():
            self.assert_true(isdir(filepath))
        elif "link" in kind.lower():
            self.assert_true(islink(filepath))

    def assert_file_doesnt_exist(self, filepath):
        "Confirm filepath doesn't exist"
        self.assert_true(not exists(filepath))

    def assert_file_contains(self, filepath, count, regex):
        "Check if filepath contains count occurances of regex"

        with open(filepath, "r") as fhandle:
            matches = sum(len(re.findall(regex, line)) for line in fhandle.xreadlines())
        self.assert_equal(count, matches)

    def assert_file_doesnt_contain(self, filepath, regex):
        "Check if filepath has 0 occurences of regex"
        return self.assert_file_contains(filepath, 0, regex)


@unittest.skipUnless(platform.linux_distribution()[0] in ["Fedora"], "Currently RPM-only packaging.")
class PackageAssertsMixin(object):
    "TestCase mixin giving assertions about the system packaging DB"

    def assert_package_not_installed(self, package_names):
        "Check if a package, or list of packages, are not installed"
        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(not self._rpm_installed(pkg))

    def assert_package_installed(self, package_names):
        "Check if a package, or list of packages, are installed"

        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(self._rpm_installed(pkg))

    def _rpm_installed(self, package_name):
        cmdline = ["/usr/bin/rpm", "-q", package_name]
        return _sudo(cmdline)

