import unittest
from sampledata import data
from src.basic import sell, buy
import copy


class TestSellMethod(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.data["cash"] = 3950

    def test_sellRealEstate(self):
        card = {
                "name": "STARTERHOUSE",
                "size": 1,
                "cost": 55000,
                "mortgage": 50000,
                "downpay": 5000,
                "value": 200,
                "key": 1,
            }
        iteration = 0
        for i in self.data["assets"]["realestate"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["realestate"])
        sell.sell(["assets", "realestate", iteration], self.data, True, 135000)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.assertEqual(1, self.data["assets"]["realestate"][0]["key"])
        self.assertEqual(self.data["cash"], 88950)

    def test_sellRealEstate2(self):
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
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.assertEqual(1, self.data["assets"]["realestate"][0]["key"])
        self.assertEqual(self.data["cash"], 95950)

    def test_sellRealEstate3(self):
        card = {
            "type": "realestate",
            "name": "APARTMENTCOMPLEX",
            "size": 30,
            "cost": 800000,
            "mortgage": 700000,
            "downpay": 100000,
            "value": 4500
        }
        iteration = 0
        self.data["cash"] = 105000
        self.data = buy.buy(card, self.data, True)
        for i in self.data["assets"]["realestate"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["realestate"])
        sell.sell(["assets", "realestate", iteration], self.data, True, 35000)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.assertEqual(1, self.data["assets"]["realestate"][0]["key"])
        self.assertEqual(self.data["cash"], 355000)

    def test_sellLand(self):
        card = {
            "name": "Land",
            "size": 20,
            "cost": 30000,
            "mortgage": 15000,
            "downpay": 15000,
            "value": -150,
            "key": 1
        }
        iteration = 0
        for i in self.data["assets"]["land"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["land"])
        sell.sell(["assets", "land", iteration], self.data, True, 150000, 10)
        self.assertEqual(10, self.data["assets"]["land"][0]["size"])
        self.assertNotIn("mortgage", self.data["assets"]["land"][0])
        self.assertEqual(138950, self.data["cash"])

    def test_sellLand2(self):
        card = {
            "name": "Land",
            "size": 20,
            "cost": 30000,
            "mortgage": 15000,
            "downpay": 15000,
            "value": -150,
            "key": 1
        }
        iteration = 0
        for i in self.data["assets"]["land"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["land"])
        sell.sell(["assets", "land", iteration], self.data, True, 40000, 5)
        self.assertEqual(15, self.data["assets"]["land"][0]["size"])
        self.assertNotIn("mortgage", self.data["assets"]["land"][0])
        self.assertEqual(28950, self.data["cash"])

    def test_sellAllLand(self):
        card = {
            "name": "Land",
            "size": 20,
            "cost": 30000,
            "mortgage": 15000,
            "downpay": 15000,
            "value": -150,
            "key": 1
        }
        iteration = 0
        for i in self.data["assets"]["land"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["land"])
        sell.sell(["assets", "land", iteration], self.data, True, 300000, 20)
        self.assertNotIn(card, self.data["assets"]["land"])
        self.assertEqual(288950, self.data["cash"])

    def test_sellPartRegularStock(self):
        buyCard = {"type": "stock", "name": "OK4U", "option": "REGULAR", "costPerShare": 1}
        sellCard = {
            "name": "OK4U",
            "option": "REGULAR",
            "amount": 1000,
            "costPerShare": 1,
            "key": len(self.data["assets"]["stock"])+1
        }
        endCard = {"name": "OK4U", "option": "REGULAR", "costPerShare": 1, "amount": 100,
                   "key": len(self.data["assets"]["stock"])+1}
        self.data = buy.buy(buyCard, self.data, True, 1000)
        iteration = 0
        for i in self.data["assets"]["stock"]:
            iteration += 1
            if i == sellCard:
                break
        self.assertIn(sellCard, self.data["assets"]["stock"])
        sell.sell(["assets", "stock", iteration], self.data, True, 40, 900)
        self.assertIn(endCard, self.data["assets"]["stock"])
        self.assertEqual(38950, self.data["cash"])

    def test_sellWholeRegularStock(self):
        sellCard = {
            "name": "OK4U",
            "option": "REGULAR",
            "amount": 1000,
            "costPerShare": 1,
            "key": 2
        }
        endCard = {"name": "OK4U", "option": "REGULAR", "costPerShare": 1, "amount": 100,
                   "key": 2}
        iteration = 0
        for i in self.data["assets"]["stock"]:
            iteration += 1
            if i == sellCard:
                break
        self.assertIn(sellCard, self.data["assets"]["stock"])
        sell.sell(["assets", "stock", iteration], self.data, True, 40, 1000)
        self.assertNotIn(endCard, self.data["assets"]["stock"])
        self.assertEqual(43950, self.data["cash"])

    def test_sellPutStock(self):
        card = {"name": "OK4U", "option": "PUT", "turns": 2, "amount": 1000, "strikePrice": 40, "costPerShare": 1,
                "key": 1}
        iteration = 0
        for i in self.data["assets"]["stock"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["stock"])
        sell.sell(["assets", "stock", iteration], self.data, True, 30)
        self.assertNotIn(card, self.data["assets"]["stock"])
        self.assertEqual(13950, self.data["cash"])

    def test_sellCallStock(self):
        card = {"name": "OK4U", "option": "CALL", "turns": 3, "amount": 1000, "strikePrice": 15, "costPerShare": 1,
                "key": 3}
        iteration = 0
        for i in self.data["assets"]["stock"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["stock"])
        sell.sell(["assets", "stock", iteration], self.data, True, 30)
        self.assertNotIn(card, self.data["assets"]["stock"])
        self.assertEqual(18950, self.data["cash"])

    def test_sellShortStock(self):
        card = {"name": "MYT4U", "option": "SHORT", "amount": 1000, "strikePrice": 50, "key": 4}
        iteration = 0
        for i in self.data["assets"]["stock"]:
            iteration += 1
            if i == card:
                break
        self.assertIn(card, self.data["assets"]["stock"])
        sell.sell(["assets", "stock", iteration], self.data, True, 30)
        self.assertNotIn(card, self.data["assets"]["stock"])
        self.assertEqual(23950, self.data["cash"])


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestSellMethod)
                   if callable(getattr(TestSellMethod, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestSellMethod(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == 'sell_test':
    runner = unittest.TextTestRunner()
    runner.run(suite())
