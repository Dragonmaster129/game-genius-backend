import unittest
from sampledata import data
from src.basic import baby
import copy


class TestBaby(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_addBaby(self):
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)
        res = baby.addBaby(self.data)
        self.assertEqual(res, "added child")
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 1)

    def test_childMarries(self):
        data.updateData(self.data)
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)
        res = baby.addBaby(self.data)
        self.assertEqual(res, "added child")
        res = baby.childMarries(self.data, 2000)
        self.assertEqual(res, "child married")
        self.assertEqual(self.data["cash"], 3070)
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)

    def test_maxChildren(self):
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)
        res = baby.addBaby(self.data)
        res = baby.addBaby(self.data)
        res = baby.addBaby(self.data)
        res = baby.addBaby(self.data)
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 3)
        self.assertEqual(res, "max amount of children")

    def test_noMarriedWhenNoChildren(self):
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)
        res = baby.childMarries(self.data, 3000)
        self.assertEqual(self.data["expenses"]["child"][0]["count"], 0)
        self.assertEqual(res, "no children")


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestBaby)
                   if callable(getattr(TestBaby, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestBaby(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "baby_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
