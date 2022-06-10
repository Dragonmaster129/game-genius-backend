import unittest
from sampledata import data
from src.markets import naturalDisaster
import copy


class TestNaturalDisaster(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData

    def test_hitTheHighestItem(self):
        self.data = naturalDisaster.disaster(self.data)


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestNaturalDisaster)
                   if callable(getattr(TestNaturalDisaster, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestNaturalDisaster(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "naturalDisaster_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
