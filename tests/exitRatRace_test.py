import unittest
from sampledata import data
from src.basic import exitRatRace
import copy


class TestExitRatRace(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_exitsWhenDoubleExpenses(self):
        data.updateData(self.data)
        self.assertFalse(exitRatRace.exitRace(self.data))
        self.data["passive"] = 99999
        self.assertTrue(exitRatRace.exitRace(self.data))


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestExitRatRace)
                   if callable(getattr(TestExitRatRace, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestExitRatRace(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "exitRatRace_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
