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

    def test_buyRealEstate(self):
        self.card = {
            "type": "realestate",
            "name": "APARTMENTCOMPLEX",
            "size": 30,
            "cost": 800000,
            "mortgage": 700000,
            "downpay": 100000,
            "value": 4500,
        }
        self.assertNotIn(self.card, self.data["assets"]["realestate"])
        self.data = buy.buy(self.card, self.data, False)
        self.assertNotIn(self.card, self.data["assets"]["realestate"])
        self.resetCashTest()
        self.data = buy.buy(self.card, self.data, True)
        self.assertIn(self.card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 4520-self.card["downpay"])

    def test_buyLand(self):
        self.card = {
                "type": "land",
                "name": "Land",
                "size": 20,
                "cost": 30000,
                "mortgage": 15000,
                "downpay": 15000,
                "value": -150,
                "key": 1
            }
        self.assertNotIn(self.card, self.data["assets"]["land"])
        self.data = buy.buy(self.card, self.data, False)
        self.assertNotIn(self.card, self.data["assets"]["land"])
        self.resetCashTest()
        self.data = buy.buy(self.card, self.data, True)
        self.assertIn(self.card, self.data["assets"]["land"])
        self.assertEqual(self.data["cash"], 4670-self.card["downpay"])


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
