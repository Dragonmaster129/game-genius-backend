from src.basic import downsized, baby, borrowLoan, buy, charity, exitRatRace, paycheck, payLoan, sell
from mongoConnection import mongoClient, getPlayerData, resetPlayer
from sampledata import data
from src.objects import player


class Game:
    def __init__(self, ID, playerList):
        self.id = ID
        self.playerList = playerList
        self.currentTurn = 0
        self.currentAction = "STARTGAME"
        self.currentCard = {}
        self.actionList = ["STARTTURN", "PAYCHECK", "OPPORTUNITY", "MARKET",
                           "DOODAD", "BABY", "CHARITY", "DOWNSIZED", "ENDTURN"]
        self.currentTarget = 0
        self.gameStarted = False

    def startGame(self):
        self.gameStarted = True

    def saveData(self, collection):
        playerList = [player1.playerData["email"] for player1 in self.playerList]
        collection.update_one({"id": self.id}, {"$set": {"playerList": playerList,
                                                         "currentTurn": self.currentTurn,
                                                         "currentAction": self.currentAction,
                                                         "currentCard": self.currentCard,
                                                         "currentTarget": self.currentTarget}})

    def nextTurn(self):
        self.currentTurn = (self.currentTurn + 1) % len(self.playerList)
        if downsized.decreaseDownsized(self.playerList[self.currentTurn].playerData["playerData"]):
            self.sendMsgToCurrentPlayer("SKIPPED")
            self.nextTurn()

    def downsizedCurrentPlayer(self):
        downsized.downsized(self.playerList[self.currentTurn].playerData["playerData"])
        self.updateData()

    def getBaby(self):
        baby.addBaby(self.playerList[self.currentTurn].playerData["playerData"])
        self.updateData()

    def borrowALoan(self, amount):
        borrowLoan.borrowLoan(self.playerList[self.currentTarget].playerData["playerData"], amount)
        self.updateData()

    def buyItem(self, card, amount, action=True):
        buy.buy(card, self.playerList[self.currentTarget].playerData["playerData"], action, amount)

    def getCharity(self):
        charity.getCharity(self.playerList[self.currentTurn].playerData["playerData"])

    def checkCharity(self):
        return charity.checkCharity(self.playerList[self.currentTurn].playerData["playerData"])

    def charityTurnEnd(self):
        charity.turnEnd(self.playerList[self.currentTurn].playerData["playerData"])

    def updateData(self):
        for playerItem in self.playerList:
            data.updateData(playerItem.playerData["playerData"])

    def playerToRightSingle(self):
        self.currentTarget = (self.currentTurn - 1) % len(self.playerList)

    def sendMsgToAllPlayers(self, msg):
        for Player in self.playerList:
            Player.sendMsg(msg)

    def sendMsgToCurrentPlayer(self, msg):
        self.playerList[self.currentTurn].sendMsg(msg)

    def sendMsgToCurrentTarget(self, msg):
        self.playerList[self.currentTarget].sendMsg(msg)

    def addPlayer(self, email, socket):
        if not self.gameStarted:
            resetPlayer.initializePlayerData(email)
            self.playerList.append(player.Player(socket, getPlayerData.getPlayerData(email)))

    def getPlayerList(self):
        return self.playerList

    def getEmailList(self):
        emailList = []
        for players in self.playerList:
            emailList.append(players.playerData["email"])
        return emailList

    def getCurrentTarget(self):
        return self.currentTarget

    def getCurrentPlayer(self):
        return self.currentTurn

    def getCurrentPlayerData(self):
        return self.playerList[self.currentTurn].playerData["playerData"]


if __name__ == "__main__":
    game = Game(10, [player.Player(1234, getPlayerData.getPlayerData("test1@test.com")),
                     player.Player(1235, getPlayerData.getPlayerData("test2@test.com"))])
    # game.saveData(mongoClient.client("cashflowDB")["game"])
    print(game.getPlayerList()[game.getCurrentPlayer()].playerData["playerData"])
    game.getBaby()
    print(game.getPlayerList()[game.getCurrentPlayer()].playerData["playerData"])
