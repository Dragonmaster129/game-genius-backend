import unittest
from sampledata import data
from src.basic import borrowLoan
import copy


class TestBorrowLoan(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.data["cash"] = 3950
        self.updateData = data.updateData

    def test_borrowLoan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 4270)
        self.assertEqual(self.data["expenses"]["loan"], 0)
        self.assertEqual(self.data["cash"], 3950)
        borrowLoan.borrowLoan(self.data, 1000)
        self.assertEqual(self.data["expenses"]["loan"], 1000)
        self.assertEqual(self.data["cash"], 4950)
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 4170)

    def test_borrowBiggerLoan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 4270)
        self.assertEqual(self.data["expenses"]["loan"], 0)
        self.assertEqual(self.data["cash"], 3950)
        borrowLoan.borrowLoan(self.data, 13000)
        self.assertEqual(self.data["expenses"]["loan"], 13000)
        self.assertEqual(self.data["cash"], 16950)
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 2970)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestBorrowLoan)
                   if callable(getattr(TestBorrowLoan, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestBorrowLoan(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "borrowLoan_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
