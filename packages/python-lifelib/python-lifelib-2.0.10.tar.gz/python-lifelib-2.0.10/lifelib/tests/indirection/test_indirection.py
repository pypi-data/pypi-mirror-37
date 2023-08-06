
import unittest
import lifelib

from lifelib.tests.integration import test_gol as tg

class TestIndirection(tg.TestGoL):

    @classmethod
    def setUpClass(cls):

        lifelib.load_rules('b3s23', force_indirect=True)

class TestIndirection2(tg.TestGoL):

    @classmethod
    def setUpClass(cls):

        lifelib.load_rules('b3s23', force_indirect=True, local_python='python2')

class TestIndirection3(tg.TestGoL):

    @classmethod
    def setUpClass(cls):

        lifelib.load_rules('b3s23', force_indirect=True, local_python='python3')

if __name__ == '__main__':
    unittest.main()
