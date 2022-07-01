import unittest
from sampledata import data
from src.markets import forcedSale
import copy


class TestForcedSale(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        data.updateData(self.data)

    def test_forcedSaleMYT4UAtZero(self):
        item = {"name": "MYT4U", "option": "SHORT", "amount": 1000, "strikePrice": 50, "key": 4}
        self.assertEqual("MYT4U", self.data["assets"]["stock"][3]["name"])
        self.assertEqual(self.data["cash"], 5070)
        forcedSale.forcedSale(["stock", "MYT4U"], self.data, 0)
        self.assertNotIn(item, self.data["assets"]["stock"])
        self.assertEqual(self.data["cash"], 55070)

    def test_forcedSaleOK4UAtFive(self):
        self.assertEqual("OK4U", self.data["assets"]["stock"][0]["name"])
        self.assertEqual(self.data["cash"], 5070)
        forcedSale.forcedSale(["stock", "OK4U"], self.data, 5)
        self.assertEqual(self.data["cash"], 10070)

    def test_forcedSaleHighestProperty(self):
        item = {
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 55000,
            "mortgage": 48000,
            "downpay": 7000,
            "value": 400,
            "key": 2,
        }
        highest = forcedSale.findHighest(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.assertIn(item, self.data["assets"]["realestate"])
        forcedSale.forcedSale(highest, self.data, self.data["assets"][highest[0]][highest[1]]["cost"])
        self.assertNotIn(item, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 12070)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestForcedSale)
                   if callable(getattr(TestForcedSale, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestForcedSale(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "forcedSale_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
