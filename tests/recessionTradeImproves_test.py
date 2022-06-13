import unittest
from sampledata import data
from src.markets import recessionTradeImproves
import copy


class TestRecessionTradeImproves(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_TradeImproves(self):
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 1120)
        recessionTradeImproves.recessionTradeImproves(self.data)
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 1300)

    def test_Recession(self):
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 1120)
        recessionTradeImproves.recessionTradeImproves(self.data, -50)
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 820)

    def test_WithNoRealEstateNoChange(self):
        self.data["assets"]["realestate"] = []
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 120)
        recessionTradeImproves.recessionTradeImproves(self.data, -50)
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 120)
        recessionTradeImproves.recessionTradeImproves(self.data, 30)
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 120)

    def test_WithLargeApartment(self):
        self.data["assets"]["realestate"] = [{
            "name": "APARTMENTCOMPLEX",
            "size": 12,
            "cost": 350000,
            "mortgage": 300000,
            "downpay": 50000,
            "value": 2000,
            "key": 1
        }]
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 2120)
        recessionTradeImproves.recessionTradeImproves(self.data, 30)
        data.updateData(self.data)
        self.assertEqual(self.data["passive"], 2480)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestRecessionTradeImproves)
                   if callable(getattr(TestRecessionTradeImproves, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestRecessionTradeImproves(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "recessionTradeImproves_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
