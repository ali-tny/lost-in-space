import unittest

class InitialisationTests(unittest.TestCase):

    def test_initialisation(self):
        """Check test suite runs by affirming 2+2=4"""
        self.assertEqual(2+2, 4)

    def test_import(self):
        """Ensure test suite can import module"""
        try:
            import startracker
        except ImportError:
            self.fail('Was not able to import startracker')
