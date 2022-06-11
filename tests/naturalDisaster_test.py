import unittest
from sampledata import data
from src.basic import sell
from src.markets import naturalDisaster
import copy


class TestNaturalDisaster(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData

    def test_hitTheHighestItem(self):
        self.data = naturalDisaster.disaster(self.data)
        self.assertIn("disaster", self.data["assets"]["realestate"][1])
        self.assertEqual(0, self.data["assets"]["realestate"][1]["value"])

    def test_sellRealEstateDisaster(self):
        self.updateData(self.data)
        # check for disaster
        card = {
            "name": "4-PLEX",
            "size": 4,
            "cost": 55000,
            "mortgage": 48000,
            "downpay": 7000,
            "value": 400,
            "key": 3,
        }
        iteration = 0
        for i in self.data["assets"]["realestate"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["realestate"])
        sell.sell(["assets", "realestate", iteration], self.data, True, 35000)
        self.data = naturalDisaster.disaster(self.data)
        card = {
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 55000,
            "mortgage": 48000,
            "downpay": 7000,
            "value": 0,
            "disaster": True,
            "key": 2,
        }
        self.assertIn(card, self.data["assets"]["realestate"])
        sell.sell(["assets", "realestate", 2], self.data, not card["disaster"], 80000)
        self.assertIn(card, self.data["assets"]["realestate"])
        card["disaster"] = False
        sell.sell(["assets", "realestate", 2], self.data, not card["disaster"], 80000)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        sell.sell(["assets", "realestate", 1], self.data, True, 80000)
        self.data["cash"] = 3950
        card = {
            "name": "Land",
            "size": 20,
            "cost": 30000,
            "mortgage": 15000,
            "downpay": 15000,
            "value": -150,
            "disaster": True,
            "key": 1
        }
        self.data = naturalDisaster.disaster(self.data)
        self.assertIn(card, self.data["assets"]["land"])
        sell.sell(["assets", "land", 1], self.data, not self.data["assets"]["land"][0]["disaster"], 150000, 10)
        self.assertIn(card, self.data["assets"]["land"])
        card["disaster"] = False
        self.data["assets"]["land"][0]["disaster"] = False
        self.assertIn(card, self.data["assets"]["land"])
        sell.sell(["assets", "land", 1], self.data, not self.data["assets"]["land"][0]["disaster"], 150000, 10)
        self.assertEqual(self.data["cash"], 138950)
        self.assertNotIn("mortgage", self.data["assets"]["land"][0])
        self.assertEqual(10, self.data["assets"]["land"][0]["size"])


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
