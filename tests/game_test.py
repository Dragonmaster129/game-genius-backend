from src.objects import game
import unittest
from sampledata import data
from src.basic import buy
from mongoConnection import mongoClient
import copy
from tests import player_test


class TestGame(game.Game):
    def saveData(self, collection):
        pass


class TestGameplay(unittest.TestCase):
    def setUp(self) -> None:
        self.db = mongoClient.client("cashflowDB")
        self.game = TestGame(10, [player_test.TestPlayer(self.db["player"].find({"email": "test1@test.com"})[0]),
                                  player_test.TestPlayer(self.db["player"].find({"email": "test2@test.com"})[0])])

    def test_addPlayer(self):
        self.assertNotIn(self.db["player"].find({"email": "test@test.com"})[0],
                         self.game.getPlayerList())
        self.game.addPlayer(self.db["player"].find({"email": "test@test.com"})[0])
        self.assertIn(self.db["player"].find({"email": "test@test.com"})[0], self.game.getPlayerList())

    def test_playerToRight(self):
        self.assertEqual(self.game.getCurrentTarget(), self.game.getCurrentPlayer())
        self.game.playerToRightSingle()
        self.assertEqual(self.game.getCurrentTarget()-1 % len(self.game.getPlayerList()), self.game.getCurrentPlayer())


def suite():
    suite = unittest.TestSuite()
    method_list = [func for func in dir(TestGameplay)
                   if callable(getattr(TestGameplay, func)) and func.startswith("test_")]
    for i in method_list:
        suite.addTest((TestGameplay(i)))
    return suite


# Change the name to the name of the file dropping the .py
if __name__ == "game_test":
    runner = unittest.TextTestRunner()
    runner.run(suite())
