#!/usr/bin/env python
# encoding: utf-8


import unittest
from craigs_python_utils.cfengine import CFEDict


class CFEDictBasicUsage(unittest.TestCase):

    def test_it_should_be_a_dictionary(self):
        self.assertIsInstance(CFEDict(), dict)

    def test_it_should_render_in_cfe_module_syntax(self):
        cfedict = CFEDict({"foo": "bar", "foo-foo": "bar-bar"})
        expected = (
            "=cfedict[foo]=bar\n"
            "=cfedict[foo_foo]=bar_bar\n"
        )
        self.assertEqual(expected, str(cfedict))

    def test_it_should_have_a_configurable_name(self):
        cfedict = CFEDict({"foo": "bar"}, cfename="Fizz")
        self.assertEqual("=Fizz[foo]=bar\n", str(cfedict))

    def test_its_name_should_default_to_the_variable_name_used_in_the_python_source(self):
        a_funny_name = CFEDict({"foo": "bar"})
        self.assertEqual("=a_funny_name[foo]=bar\n", str(a_funny_name))

    def test_it_should_provide_a_default_name_when_used_anonymously_in_python(self):
        expected = "=unparsable_python_name[foo]=bar\n"
        self.assertEqual(expected, str(CFEDict({"foo": "bar"})))


if __name__ == '__main__':
    unittest.main()
