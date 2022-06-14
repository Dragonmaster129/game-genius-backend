import unittest
from sampledata import data
from src import doodad, checkBaby
import copy


class TestDoodad(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)
        self.updateData = data.updateData

    def test_payCash(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data = doodad.doodad(self.data, cash=20)
        self.assertEqual(self.data["cash"], 5050)

    def test_payCashFlow(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data = doodad.doodad(self.data, cashflow=100)
        self.assertEqual(self.data["cash"], 5070)
        self.assertEqual(self.data["expenses"]["other"], 2980)

    def test_payCashFlowWithCategoryOther(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data = doodad.doodad(self.data, cashflow=100, category="other")
        self.assertEqual(self.data["cash"], 5070)
        self.assertEqual(self.data["expenses"]["other"], 2980)

    def test_payCashAndFlowWithCategoryCarLoan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data = doodad.doodad(self.data, cash=3000, cashflow={"monthly": 250, "totalCost": 5000}, category="car")
        self.assertEqual(self.data["cash"], 2070)
        self.assertEqual(self.data["expenses"]["car"][1], {"monthly": 250, "totalCost": 5000})

    def test_doNotPayCashIfHasNoChild(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        if checkBaby.checkBaby(self.data):
            self.data = doodad.doodad(self.data, cash=(self.data["expenses"]["child"][0]["count"] * 50))
        self.assertEqual(self.data["cash"], 5070)

    def test_payCashIfHasChild(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data["expenses"]["child"][0]["count"] = 1
        if checkBaby.checkBaby(self.data):
            self.data = doodad.doodad(self.data, cash=(self.data["expenses"]["child"][0]["count"] * 50))
        self.assertEqual(self.data["cash"], 5020)

    def test_doNotPayAndCashFlowIfHasNoChild(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        if checkBaby.checkBaby(self.data):
            self.data = doodad.doodad(self.data, cash=500, cashflow=100)
        self.assertEqual(self.data["cash"], 5070)
        self.assertEqual(self.data["expenses"]["other"], 2880)

    def test_payCashAndFlowIfHasChild(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data["expenses"]["child"][0]["count"] = 1
        if checkBaby.checkBaby(self.data):
            self.data = doodad.doodad(self.data, cash=500, cashflow=100)
        self.assertEqual(self.data["cash"], 4570)
        self.assertEqual(self.data["expenses"]["other"], 2980)

    def test_payCashAndFlowInMortgage(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data["cash"] = 30000
        self.data = doodad.doodad(self.data, cash=25000, cashflow={"monthly": 500, "totalCost": 50000},
                                  category="mortgage")
        self.assertEqual(self.data["cash"], 5000)
        self.assertEqual(self.data["expenses"]["mortgage"][1], {"monthly": 500, "totalCost": 50000})

    def test_payCashIfPassiveGreaterThan(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data["passive"] = 400
        if self.data["passive"] >= 500:
            self.data = doodad.doodad(self.data, cash=3000)
        self.assertEqual(self.data["cash"], 5070)
        self.updateData(self.data)
        if self.data["passive"] >= 500:
            self.data = doodad.doodad(self.data, cash=3000)
        self.assertEqual(self.data["cash"], 2070)

    def test_TheGoodDoodad(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.assertEqual(self.data["downsizedImmunity"], False)
        self.data = doodad.doodad(self.data, category="GOOD")
        self.assertEqual(self.data["cash"], 10070)
        self.assertEqual(self.data["downsizedImmunity"], 1)

    def test_expensive(self):
        self.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.data["cash"] = 15000
        self.data = doodad.doodad(self.data, cash=12000, cashflow={"monthly": 260, "totalCost": 20000},
                                  category="mortgage")
        self.data = doodad.doodad(self.data, cashflow=140)
        self.assertEqual(self.data["cash"], 3000)
        self.assertEqual(self.data["expenses"]["mortgage"][1], {"monthly": 260, "totalCost": 20000})
        self.assertEqual(self.data["expenses"]["other"], 3020)


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestDoodad)
                   if callable(getattr(TestDoodad, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestDoodad(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "doodad_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
