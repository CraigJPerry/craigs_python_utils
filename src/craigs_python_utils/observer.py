#!/usr/bin/env python
# encoding: utf-8


"""An observer pattern mixin.

This module exposes an implementation of the observer pattern suitable
for reuse as a mixin in python classes. By inheriting from this mixin
your object will gain a list field which will contain observers registered
with your object through its inherited method register_observer(callable).
"""


class ObserverPatternMixin(object):
    """An observer pattern implementation suitable for mixin
    use in other python classes.
    """

    def __init__(self):
        self._observers = []

    def register_observer(self, callable_observer):
        """Register a callable as an observer of this class.

        The callable can optionally receive positional and keyword
        arguments.
        """
        if not callable(callable_observer):
            raise TypeError("Can't register non-callable as an observer", callable_observer)
        self._observers.append(callable_observer)

    def unregister_observer(self, existing_observer):
        """De-register the first occurrance of existing_observer."""
        if existing_observer not in self._observers:
            return False
        self._observers.remove(existing_observer)
        return True

    def notify(self, *args, **kwargs):
        """Iterate the list of observers, calling each in turn
        until one returns True or the end of the list is reached.

        :returns: number of observers invoked
        """
        for count, observer in enumerate(self._observers, start=1):
            if observer(*args, **kwargs):
                break
        return count
