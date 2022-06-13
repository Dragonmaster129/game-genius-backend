import unittest
from sampledata import data
from src.basic import downsized
import copy


class TestDownsized(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_gotDownsized(self):
        data.updateData(self.data)
        self.assertEqual(self.data["downsized"], 0)
        res = downsized.downsized(self.data)
        self.assertEqual(res, True)
        self.assertEqual(self.data["expenses"]["loan"], 5000)
        self.assertEqual(self.data["downsized"], 2)
        self.assertEqual(self.data["cash"], 420)

    def test_decreaseDownsized(self):
        self.data["downsized"] = 2
        res = downsized.decreaseDownsized(self.data)
        self.assertEqual(res, True)
        self.assertEqual(self.data["downsized"], 1)
        res = downsized.decreaseDownsized(self.data)
        self.assertEqual(res, True)
        self.assertEqual(self.data["downsized"], 0)
        res = downsized.decreaseDownsized(self.data)
        self.assertEqual(res, False)
        self.assertEqual(self.data["downsized"], 0)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestDownsized)
                   if callable(getattr(TestDownsized, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestDownsized(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "downsized_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
