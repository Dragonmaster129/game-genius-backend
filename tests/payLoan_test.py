import unittest
from sampledata import data
from src import payLoan
import copy


class TestPayLoan(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData
        self.data["cash"] = 3950
        self.data["expenses"]["loan"] = 10000

    def test_payLoan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 3270)
        self.assertEqual(self.data["expenses"]["loan"], 10000)
        self.assertEqual(self.data["cash"], 3950)
        payLoan.payLoan(self.data, 1000)
        self.assertEqual(self.data["expenses"]["loan"], 9000)
        self.assertEqual(self.data["cash"], 2950)
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 3370)

    def test_payBiggerLoan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 3270)
        self.assertEqual(self.data["expenses"]["loan"], 10000)
        self.assertEqual(self.data["cash"], 3950)
        payLoan.payLoan(self.data, 3000)
        self.assertEqual(self.data["expenses"]["loan"], 7000)
        self.assertEqual(self.data["cash"], 950)
        self.updateData(self.data)
        self.assertEqual(self.data["cashflow"], 3570)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestPayLoan)
                   if callable(getattr(TestPayLoan, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestPayLoan(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "payLoan_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
