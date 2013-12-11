#!/usr/bin/env python
# encoding: utf-8


"""Unit testing and example usage of the ObserverPatternMixin"""


import sys
from os.path import join, dirname
sys.path.insert(0, join(dirname(__file__), ".."))
import unittest
from craigs_python_utils.observer import ObserverPatternMixin


# Fixtures


_FLAG = 0


def never_consume_observer(amount):
    """Observe notification of events but never consume them."""
    global _FLAG
    _FLAG += amount
    return False


def always_consume_observer(amount):
    """Observe notification of events and always consume them."""
    global _FLAG
    _FLAG += amount
    return True


class SimpleEventGenerator(ObserverPatternMixin):
    """Test fixture for testing of the mixin."""

    def __init__(self):
        super(SimpleEventGenerator, self).__init__()

    def do_something(self, amount=1):
        """An action warranting notification to observers."""
        self.notify(amount)


class TestObserverPatternMixin(unittest.TestCase):
    """Test usage of the observer pattern."""

    def setUp(self):
        self.seg = SimpleEventGenerator()
        global _FLAG
        _FLAG = 0

    def test_creation(self):
        """Ensure subclasses of ObserverPatternMixin can be instantiated."""
        self.assertTrue(self.seg is not None)

    def test_register_observer_valid(self):
        """Ensure valid observer can be registered with the mixin."""
        self.seg.register_observer(never_consume_observer)
        self.assertTrue(never_consume_observer in self.seg._observers)

    def test_register_observer_invalid(self):
        """Ensure invalid observer (non callable) cannot be registered
        as an observer."""
        foo = "I'm a string, i'm not callable"
        self.assertRaises(TypeError, self.seg.register_observer, foo)

    def test_register_many_observers(self):
        """Ensure multiple observers can be added to the observer list."""
        self.seg.register_observer(always_consume_observer)
        self.seg.register_observer(never_consume_observer)
        self.assertEqual(2, len(self.seg._observers))

    def test_unregister_observer_valid(self):
        """Ensure unregistering an observer works."""
        self.test_register_observer_valid()
        self.seg.unregister_observer(never_consume_observer)
        self.assertTrue(never_consume_observer not in self.seg._observers)

    def test_unregister_observer_invalid(self):
        """Ensure unregistering an observer fails as expected for invalid
        inputs."""
        self.seg.register_observer(always_consume_observer)
        removed = self.seg.unregister_observer(never_consume_observer)
        self.assertFalse(removed)

    def test_notify(self):
        """Ensure notification invokes callback to registered observer."""
        self.seg.register_observer(always_consume_observer)
        self.seg.do_something()
        self.assertEqual(1, _FLAG)

    def test_notify_many(self):
        """Ensure notification propogates to all registered observers."""
        self.seg.register_observer(never_consume_observer)
        self.seg.register_observer(always_consume_observer)
        self.seg.do_something()
        self.assertEqual(2, _FLAG)

    def test_notify_many_stops_correctly(self):
        """Ensure notification does not propogate past a consuming observer."""
        self.seg.register_observer(always_consume_observer)
        self.seg.register_observer(never_consume_observer)  # Not invoked
        self.seg.do_something()
        self.assertEqual(1, _FLAG)

    def test_notify_with_args(self):
        """Ensure args supplied propogate to observers."""
        self.seg.register_observer(never_consume_observer)
        self.seg.do_something(2)
        self.assertEqual(2, _FLAG)


if __name__ == '__main__':
    unittest.main()
