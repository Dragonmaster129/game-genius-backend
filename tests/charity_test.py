import unittest
from sampledata import data
from src.basic import charity
import copy


class TestCharity(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_charity(self):
        data.updateData(self.data)
        self.assertEqual(self.data["charity"], 0)
        res = charity.turnEnd(self.data)
        self.assertEqual(res, False)
        self.assertEqual(self.data["charity"], 0)
        res = charity.getCharity(self.data)
        self.assertEqual(res, True)
        self.assertEqual(self.data["charity"], 4)
        res = charity.turnEnd(self.data)
        self.assertEqual(res, True)
        self.assertEqual(self.data["charity"], 3)

    def test_cannotGetCharityWithNoMoney(self):
        self.data["cash"] = 0
        self.assertEqual(self.data["charity"], 0)
        res = charity.getCharity(self.data)
        self.assertEqual(res, False)
        self.assertEqual(self.data["charity"], 0)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestCharity)
                   if callable(getattr(TestCharity, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestCharity(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "charity_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
