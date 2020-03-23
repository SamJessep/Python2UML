import unittest
from py2UML import Py2UML


class TestMethods(unittest.TestCase):
    def test_upper(self):
        print('Testing upper')
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
