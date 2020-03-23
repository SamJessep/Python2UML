import unittest

#Quick fire example unit test. Gotta add these for the main app later.
class TestMethods(unittest.TestCase):
    def test_upper(self):
        #Quick fire example doctest. Gotta integrate these into the app's commands.
        """
        >>> x = 1
        >>> x
        1
        """
        print('Testing upper')
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()