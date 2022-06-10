import unittest
from src import totalUp
from sampledata import data
import copy


class TestTotalUp(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def resetUp(self):
        self.data = copy.deepcopy(data.externalData)

    def test_TotalUpBasic(self):
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 14320)
        self.assertEqual(totalUp.totalUp(self.data["expenses"]), 9650)

    def test_TotalUpCard2(self):
        self.resetUp()
        self.data["assets"]["business"].append({"name": "CARD2", "value": 500, "key": 1})
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 14320)
        self.data["assets"]["business"].append({"name": "CARD1", "cost": 200, "downpay": 200, "key": 2})
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 14820)

    def test_TotalUpCard3(self):
        self.resetUp()
        self.data["assets"]["business"].append({"name": "CARD3", "value": 5000, "key": 1})
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 14320)
        self.data["assets"]["business"].append({"name": "CARD1", "cost": 200, "downpay": 200, "key": 2})
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 14320)
        self.data["assets"]["business"].append({"name": "CARD2", "value": 500, "key": 3})
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 19820)


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestTotalUp)
                   if callable(getattr(TestTotalUp, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestTotalUp(i)))
    return suite


if __name__ == "totalUp_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
