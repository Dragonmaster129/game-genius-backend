import unittest
from sampledata import data
from src import paycheck
import copy


class TestPaycheck(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData

    def test_cashIncreased(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 4670)
        paycheck.paycheck(self.data)
        self.assertEqual(self.data["cash"], 4670 + self.data["cashflow"])


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestPaycheck)
                   if callable(getattr(TestPaycheck, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestPaycheck(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "paycheck_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
