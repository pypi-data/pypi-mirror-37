
import unittest

class TestCRT(unittest.TestCase):

    def test_cygdir(self):

        import lifelib
        lifelib.add_cygdir('something')
        from lifelib import autocompile
        self.assertEqual(autocompile.cygwin_dirs, ['something'])

if __name__ == '__main__':
    unittest.main()
