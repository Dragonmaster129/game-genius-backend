from src.objects import game
import unittest
from mongoConnection import getPlayerData, resetPlayer
from tests import player_test
import copy


class TestGame(game.Game):
    def saveData(self, collection):
        pass

    def addPlayer(self, email, socket=100):
        if not self.gameStarted:
            resetPlayer.initializePlayerData(email)
            self.playerList.append(player_test.TestPlayer(getPlayerData.getPlayerData(email)))


class TestGameplay(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TestGame(10, [player_test.TestPlayer(getPlayerData.getPlayerData("test1@test.com")),
                                  player_test.TestPlayer(getPlayerData.getPlayerData("test2@test.com"))])

    def test_startGame(self):
        self.assertFalse(self.game.gameStarted)
        self.game.startGame()
        self.assertTrue(self.game.gameStarted)

    def test_addPlayer(self):
        self.assertNotIn("test3@test.com",
                         self.game.getEmailList())
        self.game.addPlayer("test3@test.com")
        self.assertIn("test3@test.com", self.game.getEmailList())

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

    def test_nextTurn(self):
        currentTurn = copy.deepcopy(self.game.currentTurn)
        self.assertEqual(currentTurn, self.game.currentTurn)
        self.game.nextTurn()
        self.assertNotEqual(currentTurn, self.game.currentTurn)

    def test_nextTurnIfSkipped(self):
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["downsized"], 0)
        self.game.downsizedCurrentPlayer()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["downsized"], 2)
        self.game.nextTurn()
        self.assertEqual(self.game.currentTurn, 1)
        self.game.nextTurn()
        self.assertEqual(self.game.currentTurn, 1)
        self.assertEqual(self.game.playerList[0].returnMsg(), "SKIPPED")

    def test_addBaby(self):
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 0)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["expenses"]["child"][0]["count"], 0)
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 1)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["expenses"]["child"][0]["count"], 0)
        self.game.nextTurn()
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 1)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["expenses"]["child"][0]["count"], 1)

    def test_babyMaxedAt3(self):
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 0)
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 1)
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 2)
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 3)
        self.game.getBaby()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["child"][0]["count"], 3)

    def test_borrowLoan(self):
        self.assertEqual(self.game.playerList[self.game.getCurrentTarget()].playerData["playerData"]["expenses"]["loan"], 0)
        self.assertEqual(self.game.playerList[self.game.getCurrentTarget()].playerData["playerData"]["cash"], 3950)
        self.game.borrowALoan(1000)
        self.assertEqual(self.game.playerList[self.game.getCurrentTarget()]
                         .playerData["playerData"]["expenses"]["loan"], 1000)
        self.assertEqual(self.game.playerList[self.game.getCurrentTarget()]
                         .playerData["playerData"]["cash"], 4950)

    def test_buyItem(self):
        card = {
            "type": "realestate",
            "name": "DUPLEX",
            "size": 2,
            "cost": 50000,
            "mortgage": 42000,
            "downpay": 8000,
            "value": 240,
        }
        self.assertNotIn(card,
                         self.game.playerList[self.game.currentTarget].playerData["playerData"]["assets"]["realestate"])
        self.game.buyItem(card, True, 1)
        self.assertIn(card,
                      self.game.playerList[self.game.currentTarget].playerData["playerData"]["assets"]["realestate"])

    def test_getCharity(self):
        self.assertEqual(0, self.game.getCurrentPlayerData()["charity"])
        self.assertEqual(3950, self.game.getCurrentPlayerData()["cash"])
        self.game.getCharity()
        self.assertEqual(3, self.game.getCurrentPlayerData()["charity"])
        self.assertEqual(2630, self.game.getCurrentPlayerData()["cash"])

    def test_checkCharity(self):
        self.assertFalse(self.game.checkCharity())
        self.game.getCharity()
        self.assertTrue(self.game.checkCharity())

    def test_charityDecrements(self):
        self.game.getCharity()
        self.assertEqual(3, self.game.getCurrentPlayerData()["charity"])
        self.game.charityTurnEnd()
        self.assertEqual(2, self.game.getCurrentPlayerData()["charity"])
        self.game.charityTurnEnd()
        self.assertEqual(1, self.game.getCurrentPlayerData()["charity"])
        self.game.charityTurnEnd()
        self.assertEqual(0, self.game.getCurrentPlayerData()["charity"])
        self.game.charityTurnEnd()
        self.assertEqual(0, self.game.getCurrentPlayerData()["charity"])

    def test_exitRatRace(self):
        self.assertFalse(self.game.exitRatRace())
        self.game.buyItem({"type": "realestate", "value": 100000, "downpay": 1}, 1, True)
        self.assertTrue(self.game.exitRatRace())

    def test_paycheck(self):
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 3950)
        self.game.receivePaycheck()
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 7500)

    def test_payBackLoan(self):
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 3950)
        self.assertEqual(self.game.getCurrentPlayerData()["expenses"]["loan"], 0)
        self.game.borrowALoan(1000)
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 4950)
        self.assertEqual(self.game.getCurrentPlayerData()["expenses"]["loan"], 1000)
        self.game.payBackLoan()
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 3950)
        self.assertEqual(self.game.getCurrentPlayerData()["expenses"]["loan"], 0)


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
