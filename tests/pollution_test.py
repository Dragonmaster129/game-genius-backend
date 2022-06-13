import unittest
from sampledata import data
from src.markets import pollution
import copy


class TestPollution(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_loseHighestCashflow(self):
        card = {
                "name": "STARTERHOUSE",
                "size": 1,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                "value": 400,
                "key": 2,
            }
        self.assertIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 55000
        pollution.pollution(self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 5000)
        pollution.pollution(self.data)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 5000)

    def test_doNotHaveEnoughCashGetLoan(self):
        card = card = {
                "name": "STARTERHOUSE",
                "size": 1,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                "value": 400,
                "key": 2,
            }
        self.assertIn(card, self.data["assets"]["realestate"])
        self.data["cash"] = 5000
        pollution.pollution(self.data, True)
        self.assertIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 0)
        self.assertEqual(self.data["expenses"]["loan"], 45000)
        pollution.pollution(self.data)
        self.assertNotIn(card, self.data["assets"]["realestate"])
        self.assertEqual(self.data["cash"], 0)


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestPollution)
                   if callable(getattr(TestPollution, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestPollution(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "pollution_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
