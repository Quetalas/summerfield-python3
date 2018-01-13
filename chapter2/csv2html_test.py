import csv2html
import unittest


class TestProcessOptionsMethod(unittest.TestCase):

    def test_less(self):
        self.assertEqual(csv2html.process_options(),(100, '.0f'))

if __name__ == '__main__':
    unittest.main()