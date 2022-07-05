from src.objects import game
import unittest
from mongoConnection import getPlayerData
from tests import player_test


class TestGame(game.Game):
    def saveData(self, collection):
        pass


class TestGameplay(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TestGame(10, [player_test.TestPlayer(getPlayerData.getPlayerData("test1@test.com")),
                                  player_test.TestPlayer(getPlayerData.getPlayerData("test2@test.com"))])

    def test_startGame(self):
        self.assertFalse(self.game.gameStarted)
        self.game.startGame()
        self.assertTrue(self.game.gameStarted)

    def test_addPlayer(self):
        self.assertNotIn(getPlayerData.getPlayerData("test@test.com"),
                         self.game.getPlayerList())
        self.game.addPlayer(getPlayerData.getPlayerData("test@test.com"))
        self.assertIn(getPlayerData.getPlayerData("test@test.com"), self.game.getPlayerList())

    def test_cannotAddPlayerIfGameStarted(self):
        self.assertNotIn(getPlayerData.getPlayerData("test@test.com"), self.game.getPlayerList())
        self.game.startGame()
        self.game.addPlayer(getPlayerData.getPlayerData("test@test.com"))
        self.assertNotIn(getPlayerData.getPlayerData("test@test.com"), self.game.getPlayerList())

    def test_playerToRight(self):
        self.assertEqual(self.game.getCurrentTarget(), self.game.getCurrentPlayer())
        self.game.playerToRightSingle()
        self.assertEqual(self.game.getCurrentTarget()-1 % len(self.game.getPlayerList()), self.game.getCurrentPlayer())

    def test_sendMsgToCurrentPlayer(self):
        self.assertNotEqual(self.game.playerList[self.game.currentTurn].returnMsg(), "This is message.")
        self.game.sendMsgToCurrentPlayer("This is message.")
        self.assertEqual(self.game.playerList[self.game.currentTurn].returnMsg(), "This is message.")

    def test_sendMsgToCurrentTargetNotCurrentPlayer(self):
        self.game.playerToRightSingle()
        self.assertNotEqual(self.game.getCurrentTarget(), self.game.getCurrentPlayer())
        self.assertNotEqual(self.game.playerList[self.game.currentTarget].returnMsg(), "This is the message.")
        self.assertNotEqual(self.game.playerList[self.game.currentTurn].returnMsg(), "This is the message.")
        self.game.sendMsgToCurrentTarget("This is the message.")
        self.assertEqual(self.game.playerList[self.game.currentTarget].returnMsg(), "This is the message.")
        self.assertNotEqual(self.game.playerList[self.game.currentTurn].returnMsg(), "This is the message.")

    def test_sendMsdToAllPlayers(self):
        self.assertNotEqual(self.game.playerList[0].returnMsg(), "The message.")
        self.assertNotEqual(self.game.playerList[1].returnMsg(), "The message.")
        self.game.sendMsgToAllPlayers("The message.")
        self.assertEqual(self.game.playerList[0].returnMsg(), "The message.")
        self.assertEqual(self.game.playerList[1].returnMsg(), "The message.")


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