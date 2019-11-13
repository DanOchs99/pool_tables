import unittest
from table import Table
import datetime

class TestTable(unittest.TestCase):
    def test_initializer(self):
        test_table = Table(22)
        self.assertEqual(test_table.num, 22)        # just created table number 22
        self.assertEqual(test_table.status, False)  # a newly created table should be open
        self.assertIsNone(test_table.start)         # a newly created table should not have a start time

    def test_open(self):
        ### test open a table function
        test_table = Table(1)
        test_table.open()
        self.assertEqual(test_table.status, True)   # after opening table, status should be True
        self.assertIsNotNone(test_table.start)      # occupied table should have a start time
        t_delta = datetime.datetime.now() - test_table.start
        self.assertLess(t_delta.total_seconds(),5)  # should have started less than 5 seconds ago

    def test_close(self):
        ### test close out a table function
        test_table = Table(2)
        test_table.open()
        test_table.close('test_output.txt')
        self.assertEqual(test_table.status, False)  # just closed this table
        self.assertIsNone(test_table.start)         # an open table should not have a start time

if __name__ == '__main__':
    unittest.main()