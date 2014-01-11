#!/usr/bin/env python
# encoding: utf-8


"""Useful utilities when working with CFEngine 3."""

import traceback


def cfe_escape(raw):
    """Escape and munge into valid CFE syntax."""
    return raw.replace("-", "_")


class CFEDict(dict):
    """A dict that renders it's contents CFE module syntax.

    >>> module_sytnax_dict = CFEDict({"foo": "bar", "foo-foo": "bar-bar"})
    >>> print module_syntax_dict
    =module_sytnax_dict[foo]=bar
    =module_sytnax_dict[foo_foo]=bar_bar
    """

    def _get_name_from_source_code(self):
        line = traceback.extract_stack()[-3][3]
        if "=" in line:
            return line.split("=")[0].strip()
        return "unparsable_python_name"

    def __init__(self, *args, **kwargs):
        cfename = kwargs.pop("cfename", None)
        super(CFEDict, self).__init__(*args, **kwargs)
        self._cfename = cfe_escape(cfename or self._get_name_from_source_code())

    def __str__(self):
        return "\n".join(["={0}[{1}]={2}".format(self._cfename, cfe_escape(key), cfe_escape(value)) for key, value in self.iteritems()]) + "\n"
