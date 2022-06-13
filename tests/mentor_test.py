import unittest
from sampledata import data
from src.markets import mentor
import copy


class TestMentor(unittest.TestCase):
    def setUp(self) -> None:
        self.data = copy.deepcopy(data.externalData)

    def test_mentorState(self):
        self.assertEqual(self.data["mentor"], 0)
        mentor.mentor(self.data)
        self.assertEqual(self.data["mentor"], 3)
        res = mentor.decrementMentor(self.data)
        self.assertEqual(self.data["mentor"], 2)
        self.assertEqual(res, True)
        res = mentor.decrementMentor(self.data)
        self.assertEqual(self.data["mentor"], 1)
        self.assertEqual(res, True)
        res = mentor.decrementMentor(self.data)
        self.assertEqual(self.data["mentor"], 0)
        self.assertEqual(res, True)
        res = mentor.decrementMentor(self.data)
        self.assertEqual(self.data["mentor"], 0)
        self.assertEqual(res, False)


# How to run the tests when this file isn't the main
def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestMentor)
                   if callable(getattr(TestMentor, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestMentor(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "mentor_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
