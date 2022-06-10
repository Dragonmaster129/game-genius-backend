import unittest
from sampledata import data
from src.markets import insurance
import copy


class TestInsurance(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData

    def test_getInsurance(self):
        self.data = insurance.getInsurance(self.data, 200)
        self.updateData(self.data)
        self.assertEqual(self.data["expenses"]["insurance"], 200)

    def test_checkInsurance(self):
        self.data = insurance.getInsurance(self.data, 200)
        self.updateData(self.data)
        self.assertEqual(insurance.checkInsurance(self.data), True)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestInsurance)
                   if callable(getattr(TestInsurance, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestInsurance(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "insurance_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())