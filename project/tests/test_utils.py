from django.test import TestCase

from project.utils import Fork


class ForkTest(TestCase):
    def setUp(self):
        self.fork = Fork(a=False, b=False, c=True, d=False, e=True)

    def test_init_without_available_paths(self):
        with self.assertRaisesRegex(ValueError, r"No paths evaluated to True"):
            Fork(a=False, b=False, c=False, d=False, e=False)

    def test_init_with_available_paths(self):
        self.assertEqual(self.fork.paths, ["c", "e"])

    def test_call_without_available_paths(self):
        with self.assertRaisesRegex(ValueError, r"No available path to a value"):
            self.fork(a={}, b=[], d=None)

    def test_call_with_available_paths(self):
        self.assertEqual(self.fork(a=1, b=2, c=3, d=4, e=5), 3)
