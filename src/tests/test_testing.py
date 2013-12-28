#!/usr/bin/env python
# encoding: utf-8


"""Unit testing and example usage of the Pep8TestCase"""

import unittest
import platform
import os
from craigs_python_utils.testing import Pep8TestCase, FileSystemAssertsMixin, PackageAssertsMixin


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


class TestFileSystemAssertsMixinExists(Pep8TestCase, FileSystemAssertsMixin):

    def test_file_exists(self):
        self.assert_file_exists(__file__)

    def test_exist_fails_when_file_doesnt_exist(self):
        self.assert_raises(AssertionError, self.assert_file_exists, "this-file-doesnt-exist")

    def test_file_doesnt_exist(self):
        self.assert_file_doesnt_exist("foo")

    def test_doesnt_exist_fails_when_file_does_exist(self):
        self.assert_raises(AssertionError, self.assert_file_doesnt_exist, __file__)


class TestFileSystemAssertsMixinContains(Pep8TestCase, FileSystemAssertsMixin):

    def test_file_contains(self):
        self.assert_file_contains("/etc/passwd", 1, "^root")

    @unittest.skipIf(os.environ.get("TRAVIS") is None, "Travis CI machines return different results than my Fedora devbox")
    def test_file_contains_multiple_on_one_line_plus_matches_on_other_lines(self):
        self.assert_file_contains("/etc/passwd", 3, "root")

    @unittest.skipUnless(os.environ.get("TRAVIS") is None, "Travis CI machines return different results than my Fedora devbox")
    def test_file_contains_multiple_on_one_line_plus_matches_on_other_lines(self):
        self.assert_file_contains("/etc/passwd", 4, "root")

    def test_file_not_containing_expected_regex_fails(self):
        self.assert_raises(AssertionError, self.assert_file_contains, "/etc/passwd", 1, "root")

    def test_file_doesnt_contain(self):
        self.assert_file_doesnt_contain("/etc/passwd", "DonkeyKongRacer")

    def test_file_unexpectedly_containing_regex_fails(self):
        self.assert_raises(AssertionError, self.assert_file_doesnt_contain, "/etc/passwd", "root")


@unittest.skipUnless(platform.linux_distribution()[0] in ['Fedora'], "RPM-Only distributions for package management currently")
class TestPackageAssertsMixinNotInstalled(Pep8TestCase, PackageAssertsMixin):

    def test_package_not_installed(self):
        self.assert_package_not_installed("non-existant-package-name")

    def test_accepts_list_of_packages(self):
        self.assert_package_not_installed(["doesnt-exist-1", "doesnt-exist-2"])

    def test_raises_when_package_is_installed(self):
        self.assert_raises(AssertionError, self.assert_package_not_installed, "bash")

    def test_raises_when_one_package_is_installed(self):
        self.assert_raises(AssertionError, self.assert_package_not_installed, ['not-installed', 'bash'])


@unittest.skipUnless(platform.linux_distribution()[0] in ['Fedora'], "RPM-Only distributions for package management currently")
class TestPackageAssertsMixinInstalled(Pep8TestCase, PackageAssertsMixin):

    def test_package_installed(self):
        self.assert_package_installed("bash")

    def test_accepts_list_of_packages(self):
        self.assert_package_installed(["bash", "kernel"])

    def test_raises_when_package_not_installed(self):
        self.assert_raises(AssertionError, self.assert_package_installed, "not-installed")

    def test_raises_when_one_package_not_installed(self):
        self.assert_raises(AssertionError, self.assert_package_installed, ['not-installed', 'bash'])

if __name__ == '__main__':
    unittest.main()

