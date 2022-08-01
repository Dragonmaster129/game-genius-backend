from src.objects import game, player
import unittest
from mongoConnection import getPlayerData, resetPlayer, mongoClient
from tests import player_test
import copy
import time
from src.basic import downsized


class TestGame(game.Game):
    def saveData(self, collection=None):
        pass

    def addPlayer(self, email, socket=100):
        if not self.gameStarted:
            resetPlayer.initializePlayerData(email)
            self.playerList.append(player_test.TestPlayer(getPlayerData.getPlayerData(email)))

    def nextTurn(self):
        self.currentTurn = (self.currentTurn + 1) % len(self.playerList)
        self.currentTarget = copy.deepcopy(self.currentTurn)
        if downsized.decreaseDownsized(self.playerList[self.currentTurn].playerData["playerData"]):
            self.sendMsgToCurrentPlayer("SKIPPED")
            self.nextTurn()


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
        self.assertEqual(4, self.game.getCurrentPlayerData()["charity"])
        self.assertEqual(2630, self.game.getCurrentPlayerData()["cash"])

    def test_checkCharity(self):
        self.assertFalse(self.game.checkCharity())
        self.game.getCharity()
        self.assertTrue(self.game.checkCharity())

    def test_charityDecrements(self):
        self.game.getCharity()
        self.assertEqual(4, self.game.getCurrentPlayerData()["charity"])
        self.game.charityTurnEnd()
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
        self.game.payBackLoan("loan")
        self.assertEqual(self.game.getCurrentPlayerData()["cash"], 3950)
        self.assertEqual(self.game.getCurrentPlayerData()["expenses"]["loan"], 0)

    def test_sell(self):
        card = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 46000,
            "mortgage": 40000,
            "downpay": 6000,
            "value": 20,
        }
        self.game.buyItem(card, 10)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 950)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["loan"], 3000)
        self.game.sellCard(["assets", "realestate", 1], 85000, 1)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 45950)
        self.assertNotIn(card, self.game.playerList[0].playerData["playerData"]["assets"]["realestate"])

    def test_forcedSaleAll(self):
        card = {
            "type": "stock",
            "name": "OK4U",
            "option": "REGULAR",
            "costPerShare": 5,
        }
        cardCopy = {
            "type": "stock",
            "name": "OK4U",
            "option": "REGULAR",
            "costPerShare": 5,
        }
        self.game.buyItem(card, 500, True)
        self.game.nextTurn()
        self.game.buyItem(cardCopy, 500, True)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 1450)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["cash"], 1450)
        self.assertIn(card, self.game.playerList[0].playerData["playerData"]["assets"]["stock"])
        self.assertIn(cardCopy, self.game.playerList[1].playerData["playerData"]["assets"]["stock"])
        self.game.forcedSaleAll(["stock", "OK4U"], 10)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 6450)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["cash"], 6450)
        self.assertNotIn(card, self.game.playerList[0].playerData["playerData"]["assets"]["stock"])
        self.assertNotIn(card, self.game.playerList[1].playerData["playerData"]["assets"]["stock"])

    def test_saveData(self):
        TheGame = game.Game(10, [player_test.TestPlayer(getPlayerData.getPlayerData("test1@test.com")),
                                 player_test.TestPlayer(getPlayerData.getPlayerData("test2@test.com")),
                                 player_test.TestPlayer(getPlayerData.getPlayerData("test3@test.com"))])
        self.assertFalse(TheGame.playerList[0].saved)
        self.assertFalse(TheGame.playerList[1].saved)
        TheGame.saveData()
        self.assertTrue(TheGame.playerList[0].saved)
        self.assertTrue(TheGame.playerList[1].saved)
        db = mongoClient.client("cashflowDB")
        self.assertEqual(db["game"].find({"ID": 10})[0]["playerList"],
                         ["test1@test.com", "test2@test.com", "test3@test.com"])

    def test_savePlayerData(self):
        resetPlayer.initializePlayerData("test4@test.com")
        resetPlayer.initializePlayerData("test5@test.com")
        resetPlayer.initializePlayerData("test6@test.com")
        TheGame = game.Game(10, [player_test.SaveTestPlayer(getPlayerData.getPlayerData("test4@test.com")),
                                 player_test.SaveTestPlayer(getPlayerData.getPlayerData("test5@test.com")),
                                 player_test.SaveTestPlayer(getPlayerData.getPlayerData("test6@test.com"))])
        TheGame.getBaby()
        TheGame.nextTurn()
        TheGame.getCharity()
        TheGame.nextTurn()
        TheGame.downsizedCurrentPlayer()
        TheGame.saveData()
        db = mongoClient.client("cashflowDB")
        self.assertEqual(db["game"].find({"ID": 10})[0]["playerList"],
                         ["test4@test.com", "test5@test.com", "test6@test.com"])
        self.assertEqual(
            db["player"].find({"email": "test4@test.com"})[0]["playerData"]["expenses"]["child"][0]["count"],
            1
        )
        self.assertEqual(db["player"].find({"email": "test5@test.com"})[0]["playerData"]["charity"], 3)
        self.assertEqual(db["player"].find({"email": "test6@test.com"})[0]["playerData"]["downsized"], 2)

    def test_pollutionHitsPlayerToRightAll(self):
        self.game.buyItem({"type": "realestate", "name": "4PLEX", "downpay": 1, "value": 1000}, 1, True)
        self.game.nextTurn()
        self.game.buyItem({"type": "realestate", "name": "4PLEX", "downpay": 1, "value": 1000}, 1, True)
        self.game.nextTurn()
        self.assertNotEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"], [])
        self.assertNotEqual(self.game.playerList[1].playerData["playerData"]["assets"]["realestate"], [])
        # Hits the player but the player pays the 50K to keep property
        self.game.playerList[1].playerData["playerData"]["cash"] += 1
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["cash"], 3950)
        self.game.pollutionHitsPLayerToRightAll(True)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["cash"], 950)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["expenses"]["loan"], 47000)
        # Hits the player to the right of the current turn
        self.game.pollutionHitsPLayerToRightAll(False)
        self.assertNotEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"], [])
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["assets"]["realestate"], [])
        # Goes around the circle to hit the players but skips those without something in realestate
        # therefore it'll hit the original player in this two player game.
        self.game.pollutionHitsPLayerToRightAll(False)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"], [])
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["assets"]["realestate"], [])
        # If no player has any realestate then it'll terminate when it goes all the way around
        self.game.pollutionHitsPLayerToRightAll(False)

    def test_recessionTradeImproves(self):
        card = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 55000,
            "mortgage": 50000,
            "downpay": 5000,
            "value": 200,
        }
        card2 = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 55000,
            "mortgage": 48000,
            "downpay": 7000,
            "value": 400,
        }
        card3 = {
            "type": "realestate",
            "name": "4-PLEX",
            "size": 4,
            "cost": 55000,
            "mortgage": 48000,
            "downpay": 7000,
            "value": 400,
        }
        self.game.buyItem(card, 1, True)
        self.game.buyItem(card2, 1, True)
        self.game.nextTurn()
        self.game.buyItem(card3, 1, True)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["passive"], 600)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["passive"], 400)
        self.game.recessionTradeImproves(-50)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["passive"], 500)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["passive"], 200)
        self.game.recessionTradeImproves(30)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["passive"], 560)
        self.assertEqual(self.game.playerList[1].playerData["playerData"]["passive"], 320)

    def test_REUpgrade(self):
        card = {"type": "realestate", "name": "4-PLEX", "downpay": 0, "value": 300, "mortgage": 150000, "cost": 150000}
        newCard = {"name": "8-PLEX", "downpay": 40000, "value": 1700, "mortgage": 150000, "cost": 190000}
        self.game.buyItem(card, 1, True)
        self.assertIn(card, self.game.playerList[0].playerData["playerData"]["assets"]["realestate"])
        # Doesn't have the right item to upgrade so it'll fail
        self.game.REUpgrade(newCard, "DUPLEX")
        self.assertIn(card, self.game.playerList[0].playerData["playerData"]["assets"]["realestate"])
        # Has an item that will upgrade so it should upgrade
        self.game.REUpgrade(newCard, "4-PLEX")
        self.assertIn(newCard, self.game.playerList[0].playerData["playerData"]["assets"]["realestate"])

    def test_checkBaby(self):
        self.assertFalse(self.game.checkBaby())
        self.game.nextTurn()
        self.assertFalse(self.game.checkBaby())
        self.game.getBaby()
        self.assertTrue(self.game.checkBaby())

    def test_doodad(self):
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["other"], 2880)
        self.game.doodad(None, 500, "other")
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["other"], 3380)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 3950)
        self.game.doodad(20)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 3930)

    def test_resetKeyValues(self):
        self.game.playerList[0].playerData["playerData"]["assets"]["realestate"].append({
                "name": "4-PLEX",
                "size": 4,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                "value": 400,
                "key": 3,
            })
        self.assertNotEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["key"], 1)
        self.game.updateData()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["key"], 1)

    def test_getInsurance(self):
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["insurance"], 0)
        self.game.getInsurance(200)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["expenses"]["insurance"], 200)

    def test_drawCardDoodad(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "DOODAD"
        self.game.drawCard()
        self.assertNotEqual(self.game.currentCard, {})

    def test_drawCardMarket(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "MARKET"
        self.game.drawCard()
        self.assertNotEqual(self.game.currentCard, {})

    def test_drawCardBeginning(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "BEGINNING"
        self.game.drawCard()
        self.assertNotEqual(self.game.currentCard, {})

    def test_drawCardCapital(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "CAPITALGAIN"
        self.game.drawCard()
        self.assertNotEqual(self.game.currentCard, {})

    def test_drawCardCashflow(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "CASHFLOW"
        self.game.drawCard()
        self.assertNotEqual(self.game.currentCard, {})

    def test_drawCardResetList(self):
        self.assertEqual(self.game.currentCard, {})
        self.game.startGame()
        self.game.currentAction = "CAPITALGAIN"
        Onecard = self.game.capitalOrder.pop(0)
        self.game.capitalOrder = [copy.deepcopy(Onecard)]
        self.game.drawCard()
        self.assertNotEqual(self.game.capitalOrder, [])
        self.game.currentAction = "CASHFLOW"
        Onecard = self.game.cashflowOrder.pop(0)
        self.game.cashflowOrder = [copy.deepcopy(Onecard)]
        self.game.drawCard()
        self.assertNotEqual(self.game.cashflowOrder, [])

    def test_mentor(self):
        self.game.startGame()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["mentor"], 0)
        self.game.getMentor()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["mentor"], 3)
        self.game.currentAction = "CAPITALGAIN"
        self.game.drawCard()
        cardCopy = copy.deepcopy(self.game.currentCard)
        self.game.mentorAction()
        self.assertNotEqual(cardCopy, self.game.currentCard)

    def test_checkInsurance(self):
        self.assertFalse(self.game.checkInsurance())
        self.game.getInsurance(200)
        self.assertTrue(self.game.checkInsurance())

    def test_naturalDisaster(self):
        card = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 46000,
            "mortgage": 40000,
            "downpay": 6000,
            "value": 20,
        }
        self.game.buyItem(card, 1)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["value"], 20)
        self.game.naturalDisaster()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["value"], 0)

    def test_naturalDisasterInsured(self):
        card = {
            "type": "realestate",
            "name": "STARTERHOUSE",
            "size": 1,
            "cost": 46000,
            "mortgage": 40000,
            "downpay": 6000,
            "value": 20,
        }
        self.game.playerList[0].playerData["playerData"]["cash"] = 6950
        self.game.buyItem(card, 1)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["value"], 20)
        self.game.getInsurance(200)
        self.game.naturalDisaster()
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["assets"]["realestate"][0]["value"], 0)
        self.assertEqual(self.game.playerList[0].playerData["playerData"]["cash"], 6950)




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
    resetPlayer.initializePlayerData("test1@test.com", "Doctor")
    resetPlayer.initializePlayerData("test2@test.com", "Doctor")
    resetPlayer.initializePlayerData("test3@test.com", "Doctor")
    resetPlayer.initializePlayerData("test4@test.com", "Doctor")
    resetPlayer.initializePlayerData("test5@test.com", "Doctor")
    resetPlayer.initializePlayerData("test6@test.com", "Doctor")
    db = mongoClient.client("cashflowDB")["game"]
    Game = db.find({"ID": 10})
    try:
        Game[0]["playerList"]
    except IndexError:
        db.insert_one({"name": "test",
            "ID": 10,
            "timeStamp": time.time(),
            "playerList": [],
            "currentAction": "STARTGAME",
            "currentCard": {},
            "currentTarget": 0,
            "currentTurn": 0,
            "beginningOrder": [],
            "capitalOrder": [],
            "cashflowOrder": [],
            "doodadOrder": [],
            "marketOrder": [],
            "gameStarted": False,
        })
    runner.run(suite())
