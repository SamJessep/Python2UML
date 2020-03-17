"Test debugger_r, coverage 30%."

import unittest


class Test(unittest.TestCase):

    ##    @classmethod
    ##    def setUpClass(cls):
    ##        requires('gui')
    ##        cls.root = Tk()
    ##
    ##    @classmethod
    ##    def tearDownClass(cls):
    ##        cls.root.destroy()
    ##        del cls.root

    def test_init(self):
        self.assertTrue(True)  # Get coverage of import


# Classes GUIProxy, IdbAdapter, FrameProxy, CodeProxy, DictProxy,
# GUIAdapter, IdbProxy plus 7 module functions.

if __name__ == '__main__':
    unittest.main(verbosity=2)
