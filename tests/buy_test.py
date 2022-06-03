import unittest
from sampledata import data
from src import buy


class TestBuyMethod(unittest.TestCase):
    def setUp(self) -> None:
        self.data = data.externalData
        self.updateData = data.updateData
        self.updateData(self.data)

    def resetCashTest(self):
        self.updateData(self.data)
        self.data["cash"] = self.data["cashflow"] + self.data["savings"]

    def test_addData(self):
        self.assertEqual(self.data, data.externalData)

    def test_buyApartmentComplex(self):
        card = {
            "type": "realestate",
            "name": "APARTMENTCOMPLEX",
            "size": 30,
            "cost": 800000,
            "mortgage": 700000,
            "downpay": 100000,
            "value": 4500,
        }
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 105000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 105000-card["downpay"]*1)

    def test_buyDuplex(self):
        card = {
            "type": "realestate",
            "name": "DUPLEX",
            "size": 2,
            "cost": 50000,
            "mortgage": 42000,
            "downpay": 8000,
            "value": 240,
        }
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 10000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 10000-card["downpay"]*1)

    def test_buyStarterHouse(self):
        card = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 46000,
            "mortgage": 40000,
            "downpay": 6000,
            "value": 20,
        }
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 8000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 8000-card["downpay"]*1)

    def test_buy4Plex(self):
        card = {
            "type": "realestate",
            "name": "4-PLEX",
            "size": 4,
            "cost": 80000,
            "mortgage": 64000,
            "downpay": 16000,
            "value": 750,
        }
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 20000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 20000-card["downpay"]*1)

    def test_buy8Plex(self):
        card = {
            "type": "realestate",
            "name": "8-PLEX",
            "size": 8,
            "cost": 200000,
            "mortgage": 160000,
            "downpay": 40000,
            "value": 1600,
        }
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 50000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 50000-card["downpay"]*1)

    def test_buyLand(self):
        card = {
                "type": "land",
                "name": "Land",
                "size": 20,
                "cost": 30000,
                "mortgage": 15000,
                "downpay": 15000,
                "value": -150,
                "key": 1
            }
        self.assertNotIn(card, self.data["assets"]["land"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["land"])
        self.data["cash"] = 20000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["land"])
        self.assertEqual(self.data["cash"], 20000-card["downpay"]*1)

    def test_buyDividend(self):
        card = {
            "type": "dividends",
            "name": "Long Term Bonds",
            "cost": 25000,
            "downpay": 25000,
            "value": 380,
            "key": 1
        }
        shortenedCard = {
            "name": "Long Term Bonds",
            "value": 3800,
            "key": 2
        }
        self.assertNotIn(card, self.data["assets"]["dividends"])
        self.data = buy.buy(card, self.data, False, 10)
        self.assertNotIn(shortenedCard, self.data["assets"]["dividends"])
        self.data["cash"] = 255000
        self.data = buy.buy(card, self.data, True, 10)
        self.assertIn(shortenedCard, self.data["assets"]["dividends"])
        self.assertEqual(self.data["cash"], 255000-card["downpay"]*10)
        
    def test_buyRegularStock(self):
        card = {
            "type": "stock",
            "name": "OK4U",
            "option": "REGULAR",
            "costPerShare": 5,
        }
        endcard = {
            "name": "OK4U",
            "option": "REGULAR",
            "amount": 1000,
            "costPerShare": 5,
            "key": len(self.data["assets"]["stock"]) + 1
        }
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data = buy.buy(card, self.data, False, 1000)
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data["cash"] = 6000
        self.data = buy.buy(card, self.data, True, 1000)
        self.assertIn(endcard, self.data["assets"]["stock"])
        self.assertEqual(self.data["cash"], 6000 - card["costPerShare"] * 1000)

    def test_buyPutStock(self):
        card = {
            "type": "stock",
            "name": "MYT4U",
            "option": "PUT",
            "costPerShare": 2,
            "strikePrice": 35
        }
        endcard = {
            "name": "MYT4U",
            "option": "PUT",
            "turns": 3,
            "amount": 1000,
            "costPerShare": 2,
            "strikePrice": 35,
            "key": len(self.data["assets"]["stock"]) + 1
        }
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data = buy.buy(card, self.data, False, 1000)
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data["cash"] = 3000
        self.data = buy.buy(card, self.data, True, 1000)
        self.assertIn(endcard, self.data["assets"]["stock"])
        self.assertEqual(self.data["cash"], 3000 - card["costPerShare"] * 1000)

    def test_buyCallStock(self):
        card = {
            "type": "stock",
            "name": "MYT4U",
            "option": "CALL",
            "costPerShare": 2,
            "strikePrice": 15
        }
        endcard = {
            "name": "MYT4U",
            "option": "CALL",
            "turns": 3,
            "amount": 1000,
            "costPerShare": 2,
            "strikePrice": 15,
            "key": len(self.data["assets"]["stock"]) + 1
        }
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data = buy.buy(card, self.data, False, 1000)
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data["cash"] = 3000
        self.data = buy.buy(card, self.data, True, 1000)
        self.assertIn(endcard, self.data["assets"]["stock"])
        self.assertEqual(self.data["cash"], 3000 - card["costPerShare"] * 1000)

    def test_buyShortStock(self):
        card = {
            "type": "stock",
            "name": "MYT4U",
            "option": "SHORT",
            "costPerShare": 40,
        }
        endcard = {
            "name": "MYT4U",
            "option": "SHORT",
            "amount": 1000,
            "costPerShare": 40,
            "key": len(self.data["assets"]["stock"]) + 1
        }
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data = buy.buy(card, self.data, False, 1000)
        self.assertNotIn(endcard, self.data["assets"]["stock"])
        self.data["cash"] = 3000
        self.data = buy.buy(card, self.data, True, 1000)
        self.assertIn(endcard, self.data["assets"]["stock"])
        self.assertEqual(self.data["cash"], 3000)

    def test_buyD2Y1(self):
        card = {
            "type": "business",
            "name": "CARD1",
            "cost": 200,
            "downpay": 200
        }
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data["cash"] = 1000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["business"])
        self.assertEqual(self.data["cash"], 1000 - card["downpay"])

    def test_buyD2Y2(self):
        card = {
            "type": "business",
            "name": "CARD2",
            "value": 500
        }
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data["cash"] = 1000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["business"])
        self.assertEqual(self.data["cash"], 1000)

    def test_buyD2Y3(self):
        card = {
            "type": "business",
            "name": "CARD3",
            "value": 5000
        }
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data = buy.buy(card, self.data, False)
        self.assertNotIn(card, self.data["assets"]["business"])
        self.data["cash"] = 1000
        self.data = buy.buy(card, self.data, True)
        self.assertIn(card, self.data["assets"]["business"])
        self.assertEqual(self.data["cash"], 1000)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestBuyMethod)
                   if callable(getattr(TestBuyMethod, func)) and func.startswith("test")]
    for i in method_list:
        suite.addTest((TestBuyMethod(i)))
    return suite


if __name__ == "buy_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
