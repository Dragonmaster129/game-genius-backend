import unittest
from sampledata import data
from src.markets import REUpgrade
import copy


class TestMentor(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_has4PlexToChange(self):
        res = REUpgrade.upgrade(None, self.data, "4-PLEX")
        self.assertTrue(res)

    def test_doesNotHave8PlexToChange(self):
        res = REUpgrade.upgrade(None, self.data, "8-PLEX")
        self.assertFalse(res)

    def test_change4PlexTo8Plex(self):
        item = {
            "name": "8-PLEX",
            "size": 8,
            "cost": 190000,
            "mortgage": 150000,
            "downpay": 40000,
            "value": 1700,
            "key": 3
        }
        oldItem = {
                "name": "4-PLEX",
                "size": 4,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                "value": 400,
                "key": 3,
            }
        data.updateData(self.data)
        self.assertEqual(self.data["cash"], 5070)
        self.assertNotIn(item, self.data["assets"]["realestate"])
        self.assertIn(oldItem, self.data["assets"]["realestate"])
        res = REUpgrade.upgrade(item, self.data, "4-PLEX", 3)
        self.assertEqual(self.data["cash"], 5070)
        self.assertIn(item, self.data["assets"]["realestate"])
        self.assertNotIn(oldItem, self.data["assets"]["realestate"])


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestMentor)
                   if callable(getattr(TestMentor, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestMentor(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "REUpgrade_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
