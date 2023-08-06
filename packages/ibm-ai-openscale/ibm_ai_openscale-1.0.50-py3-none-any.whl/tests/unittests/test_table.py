import unittest
from ibm_ai_openscale.base_classes import Table


class TestTable(unittest.TestCase):
    def test_01_test_too_long_table(self):
        Table(
            ['uid', 'name', 'type', 'text'],
            [
                ['123456788903248623487492784329874', 'Very, very, Very, very, Very, very long name, Very, very, Very, very, Very, very long name', 'comment', 'Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be,'],
                ['123456788903248623487492784329874', 'Very, very, Very, very, Very, very long name, Very, very, Very, very, Very, very long name', 'comment',
                 'Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be, Be or not to be,']
            ]
        ).list() # TODO add check

if __name__ == '__main__':
    unittest.main()
