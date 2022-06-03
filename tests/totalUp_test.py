import unittest
from src import totalUp
from sampledata import data
import copy


class TestTotalUp(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_TotalUpBasic(self):
        self.assertEqual(totalUp.totalUp(self.data["assets"]), 13920)


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestTotalUp)
                   if callable(getattr(TestTotalUp, func)) and func.startswith("test")]
    for i in method_list:
        suite.addTest((TestTotalUp(i)))
    return suite


if __name__ == "totalUp_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
