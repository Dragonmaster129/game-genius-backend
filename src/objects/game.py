from src.basic import downsized, baby, borrowLoan, buy, charity, exitRatRace, paycheck, payLoan, sell
from src.markets import forcedSale, insurance, mentor, naturalDisaster, pollution, recessionTradeImproves, REUpgrade
from src import checkBaby, doodad, resetKeyValues
from mongoConnection import mongoClient, getPlayerData, resetPlayer
from sampledata import data
from src.objects import player
import copy
import random
import time


class Game:
    def __init__(self, ID, playerList):
        self.id = ID
        self.playerList = playerList
        self.currentTurn = 0
        self.currentAction = "STARTGAME"
        self.currentCard = {}
        self.actionList = ["STARTTURN", "PAYCHECK", "CASHFLOW", "CAPITALGAIN", "MARKET",
                           "DOODAD", "BABY", "CHARITY", "DOWNSIZED", "ENDTURN"]
        self.currentTarget = 0
        self.doodadOrder = []
        self.marketOrder = []
        self.capitalOrder = []
        self.cashflowOrder = []
        self.beginningOrder = []
        self.gameStarted = False

    def startGame(self):
        db = mongoClient.client("cashflowDB")
        Doodad = db["doodad"]
        tmpList = Doodad.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        self.doodadOrder = copy.deepcopy(List)
        Market = db["market"]
        tmpList = Market.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        self.marketOrder = copy.deepcopy(List)
        Capital = db["capitalgain"]
        tmpList = Capital.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        self.capitalOrder = copy.deepcopy(List)
        Cashflow = db["cashflow"]
        tmpList = Cashflow.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        self.cashflowOrder = copy.deepcopy(List)
        Beginning = db["beginning"]
        tmpList = Beginning.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        self.beginningOrder = copy.deepcopy(List)
        self.gameStarted = True
        self.changeAction("BEGINNING")
        for i in self.playerList:
            self.drawCard()
            self.actOnCard()
            self.nextTurn()
        self.sendMsgToAllPlayers({"EVENT": "Game started"})
        self.currentAction = "STARTTURN"
        self.sendMsgToCurrentPlayer({"EVENT": "STARTTURN"})
        self.saveData()

    def changeAction(self, action):
        if action in self.actionList or action == "BEGINNING":
            self.currentAction = action
            self.sendMsgToCurrentPlayer({"EVENT": self.currentAction})

    def fillCardDraws(self):
        search = mongoClient.client("cashflowDB")[self.currentAction.lower()]
        tmpList = search.find({}, {"_id": 0, "ID": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["ID"])
                iteration += 1
            except IndexError:
                break
        random.shuffle(List)
        if self.currentAction == "DOODAD":
            self.doodadOrder = copy.deepcopy(List)
        elif self.currentAction == "CASHFLOW":
            self.cashflowOrder = copy.deepcopy(List)
        elif self.currentAction == "CAPITALGAIN":
            self.capitalOrder = copy.deepcopy(List)
        elif self.currentAction == "MARKET":
            self.marketOrder = copy.deepcopy(List)
        elif self.currentAction == "BEGINNING":
            self.beginningOrder = copy.deepcopy(List)

    def drawCard(self):
        if self.currentAction not in ["STARTTURN", "PAYCHECK", "BABY", "CHARITY", "DOWNSIZED", "ENDTURN"]:
            db = mongoClient.client("cashflowDB")[self.currentAction.lower()]
            nextCard = ""
            if self.currentAction == "DOODAD":
                nextCard = self.doodadOrder.pop(0)
                if not self.doodadOrder:
                    self.fillCardDraws()
            elif self.currentAction == "CASHFLOW":
                nextCard = self.cashflowOrder.pop(0)
                if not self.cashflowOrder:
                    self.fillCardDraws()
            elif self.currentAction == "CAPITALGAIN":
                nextCard = self.capitalOrder.pop(0)
                if not self.capitalOrder:
                    self.fillCardDraws()
            elif self.currentAction == "MARKET":
                nextCard = self.marketOrder.pop(0)
                if not self.marketOrder:
                    self.fillCardDraws()
            elif self.currentAction == "BEGINNING":
                nextCard = self.beginningOrder.pop(0)
                if not self.beginningOrder:
                    self.fillCardDraws()
            self.currentCard = db.find({"ID": nextCard})[0]

    def actOnCard(self, playerOptions=None):
        if playerOptions is None:
            playerOptions = {}
        if self.currentAction == "BEGINNING":
            self.playerList[self.currentTurn].addBeginningCard(self.currentCard)
        elif self.currentAction == "DOODAD":
            self.doodad(cash=playerOptions["cash"], cashflow=playerOptions["cashflow"],
                        category=playerOptions["category"])
        elif self.currentAction == "MARKET":
            # market = {
            #     "title": str,  # The bold words at the top of the card
            #     "description": str,  # exactly what is on the card telling you what to do
            #     "type": str,  # eg. realestate, stock, land, business, dividend, insurance, child marries, (CONTINUED.)
            #     # pollution, natural disaster, CHARITY, mentor
            #     "name": str,  # eg. MYT4U, OK4U, 4-PLEX, STARTERHOUSE, APARTMENTCOMPLEX, ALL. What card affects
            #     "highest": bool,  # when realestate, affects the highest value of property
            #     "price": int or str,
            #     # eg. the stock price, what you are selling realestate for per unit, land. (CONTINUED.)
            #     # when child marries pay amount.
            #     "bankrupt": bool,  # eg. stock fails, lose all shares
            #     "size": int,  # in land, selling 5 acres or 10 acres
            #     "value": int,  # in spare time co, you get a $7000 value, foreign trade and recession will have this too
            #     "property": object,  # exchange deals, your starter house changes to 4-PLEX, record these new numbers.
            #     "forcedSale": bool,  # You have no choice but to sell.
            #     "target": str,
            #     # eg. Player, player your right, everyone, right all, starts with you and moves to the right.
            # }
            sellTypes = ["realestate", "stock", "land"]
            if self.currentCard["type"] in sellTypes:
                self.sellCard(playerOptions[0:2], self.currentCard["price"], playerOptions[3], self.currentCard["name"])
        elif self.currentAction == "CAPITALGAIN":
            self.buyItem(self.currentCard["card"], 1)

    def sendPlayerTheirOptions(self):
        optionsCard = {"description": self.currentCard["description"], "title": self.currentCard["title"]}
        if self.currentAction != "DOODAD":
            try:
                if self.currentCard["card"]["type"] == "realestate":
                    optionsCard["options"] = ["Buy", "Don't buy"]
                elif self.currentCard["card"]["type"] == "d2y":
                    if self.currentCard["card"]["name"] == "CARD1":
                        optionsCard["options"] = ["Buy", "Don't buy"]
                    else:
                        optionsCard["options"] = ["Buy"]
                elif self.currentCard["card"]["type"] == "royalty":
                    optionsCard["options"] = ["Buy", "Don't buy"]
                elif self.currentCard["card"]["type"] == "dividend":
                    optionsCard["options"] = ["Amount", "Buy", "Don't Buy"]
                try:
                    if self.currentCard["card"]['type'] == "stock":
                        if self.currentCard["card"]["option"] == "regular":
                            optionsCard["options"] = ["Amount", "Buy", "Sell", "Short", "Do nothing"]
                except KeyError:
                    print(self.currentCard)
            except KeyError:
                if self.currentCard["type"] == "realestate":
                    if self.currentAction == "MARKET":
                        optionsCard["options"] = ["Sell all", "Sell", "Don't Sell"]
                elif self.currentCard["type"] == "realestate Exchange":
                    if self.currentAction == "MARKET":
                        optionsCard["options"] = ["Take", "Don't take it"]
        else:
            optionsCard["options"] = ["OK"]
        return optionsCard

    def sendPlayerCharityOptions(self):
        optionsCard = {"description": "Charity costs 10% of your total income", "title": "Donate to Charity",
                       "options": ["Give", "Don't"]}
        return optionsCard

    def sendPlayerBabyOptions(self):
        optionsCard = {"description": "Add a child to your game card", "title": "You got a Baby!", "options": ["OK"]}
        return optionsCard

    def sendPlayerDownsizedOptions(self):
        optionsCard = {"description": "Lose two turns and pay your expenses", "title": "Your company downsized",
                       "options": ["OK"]}
        return optionsCard

    def saveData(self, collection=None):
        if collection is None:
            collection = mongoClient.client("cashflowDB")["game"]
        self.updateData()
        playerList = [player1.playerData["email"] for player1 in self.playerList]
        collection.update_one({"ID": self.id}, {"$set": {
            "playerList": playerList,
            "timeStamp": time.time(),
            "currentTurn": self.currentTurn,
            "currentAction": self.currentAction,
            "currentCard": self.currentCard,
            "currentTarget": self.currentTarget,
            "doodadOrder": self.doodadOrder,
            "marketOrder": self.marketOrder,
            "capitalOrder": self.capitalOrder,
            "cashflowOrder": self.cashflowOrder,
            "beginningOrder": self.beginningOrder,
            "gameStarted": self.gameStarted
        }})
        self.sendSaveEventToPlayers()

    def nextTurn(self):
        if self.checkCharity():
            self.charityTurnEnd()
        self.currentTurn = (self.currentTurn + 1) % len(self.playerList)
        self.currentTarget = copy.deepcopy(self.currentTurn)
        if self.currentAction != "BEGINNING":
            self.sendMsgToCurrentPlayer({"EVENT": "STARTTURN"})
        if downsized.decreaseDownsized(self.playerList[self.currentTurn].playerData["playerData"]):
            self.sendMsgToCurrentPlayer("SKIPPED")
            self.nextTurn()

    def resetTarget(self):
        self.currentTarget = copy.deepcopy(self.currentTurn)

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
        self.updateData()

    def getCharity(self):
        charity.getCharity(self.playerList[self.currentTurn].playerData["playerData"])
        self.updateData()

    def checkCharity(self):
        return charity.checkCharity(self.playerList[self.currentTurn].playerData["playerData"])

    def charityTurnEnd(self):
        charity.turnEnd(self.playerList[self.currentTurn].playerData["playerData"])

    def exitRatRace(self):
        self.updateData()
        return exitRatRace.exitRace(self.playerList[self.currentTurn].playerData["playerData"])

    def receivePaycheck(self):
        paycheck.paycheck(self.playerList[self.currentTurn].playerData["playerData"])
        self.updateData()

    def payBackLoan(self, amount=1000):
        payLoan.payLoan(self.playerList[self.currentTurn].playerData["playerData"], amount)
        self.updateData()

    def sellCard(self, itemData, price, amount, sellType):
        try:
            if (self.playerList[self.currentTarget]
                    .playerData["playerData"][itemData[0]][itemData[1]][itemData[2]-1]["name"]) == sellType:
                sell.sell(itemData, self.playerList[self.currentTarget].playerData["playerData"], True, price, amount)
        except KeyError:
            pass
        # itemData, data, playerAction, price, amount

    def forcedSaleAll(self, cardType, price):
        for player1 in self.playerList:
            forcedSale.forcedSale(cardType, player1.playerData["playerData"], price)

    def findFirstValue(self, cardType):
        return forcedSale.findFirstIteration(self.playerList[self.currentTarget].playerData["playerData"], cardType)

    def forcedSaleTarget(self, cardType, price):
        forcedSale.forcedSale(cardType, self.playerList[self.currentTarget].playerData["playerData"], price)

    def getMentor(self):
        mentor.mentor(self.playerList[self.currentTurn].playerData["playerData"])

    def mentorAction(self):
        mentor.decrementMentor(self.playerList[self.currentTurn].playerData["playerData"])
        self.drawCard()

    def getInsurance(self, monthlyCost):
        if self.playerList[self.currentTurn].playerData["playerData"]["expenses"]["insurance"] == 0:
            insurance.getInsurance(self.playerList[self.currentTurn].playerData["playerData"], monthlyCost)

    def checkInsurance(self):
        return insurance.checkInsurance(self.playerList[self.currentTarget].playerData["playerData"])

    def pollutionHitsPLayerToRightAll(self, payTheFiftyK=None):
        while True:
            self.currentTarget = (self.currentTarget + 1) % len(self.playerList)
            try:
                if self.playerList[self.currentTarget].playerData["playerData"]["assets"]["realestate"][0]:
                    if not insurance.checkInsurance(self.playerList[self.currentTarget].playerData["playerData"]):
                        if payTheFiftyK is None:
                            self.sendMsgToCurrentTarget("Select to pay $50000 or to lose property")
                        pollution.pollution(self.playerList[self.currentTarget].playerData["playerData"], payTheFiftyK)
                        break
                    elif insurance.checkInsurance(self.playerList[self.currentTarget].playerData["playerData"]):
                        break
            except IndexError:
                if self.currentTarget == self.currentTurn:
                    break
        self.updateData()

    def recessionTradeImproves(self, amount=30):
        for players in self.playerList:
            recessionTradeImproves.recessionTradeImproves(players.playerData["playerData"], amount)
        self.updateData()

    def REUpgrade(self, changeTo, requiredType, changing=None):
        REUpgrade.upgrade(changeTo, self.playerList[self.currentTarget].playerData["playerData"],
                          requiredType, changing)

    def checkBaby(self):
        return checkBaby.checkBaby(self.playerList[self.currentTarget].playerData["playerData"])

    def doodad(self, cash=None, cashflow=None, category=None):
        doodad.doodad(self.playerList[self.currentTurn].playerData["playerData"], cash, cashflow, category)
        self.updateData()

    def naturalDisaster(self):
        naturalDisaster.disaster(self.playerList[self.currentTarget].playerData["playerData"], self.checkInsurance())

    def updateData(self):
        for playerItem in self.playerList:
            data.updateData(playerItem.playerData["playerData"])
            for category in playerItem.playerData["playerData"]["assets"]:
                if isinstance(playerItem.playerData["playerData"]["assets"][category], list):
                    resetKeyValues.resetKeyValues(playerItem.playerData["playerData"]["assets"][category])
        self.resetTarget()

    def playerToRightSingle(self):
        self.currentTarget = (self.currentTurn - 1) % len(self.playerList)

    def sendMsgToAllPlayers(self, msg):
        for Player in self.playerList:
            Player.sendMsg(msg)

    def sendMsgToCurrentPlayer(self, msg):
        self.playerList[self.currentTurn].sendMsg(msg)

    def sendMsgToCurrentTarget(self, msg):
        self.playerList[self.currentTarget].sendMsg(msg)

    def sendSaveEventToPlayers(self, collection=None):
        if collection is None:
            collection = mongoClient.client("cashflowDB")["player"]
        for players in self.playerList:
            players.saveData(collection)

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

    def loadSaveData(self, sockets, collection=None):
        if collection is None:
            collection = mongoClient.client("cashflowDB")["game"]
        loadingGame = collection.find({"ID": self.id})[0]
        self.currentTarget = loadingGame["currentTarget"]
        self.currentTurn = loadingGame["currentTurn"]
        self.currentCard = loadingGame["currentCard"]
        self.currentAction = loadingGame["currentAction"]
        self.currentTarget = loadingGame["currentTarget"]
        self.doodadOrder = loadingGame["doodadOrder"]
        self.marketOrder = loadingGame["marketOrder"]
        self.capitalOrder = loadingGame["capitalOrder"]
        self.cashflowOrder = loadingGame["cashflowOrder"]
        self.beginningOrder = loadingGame["beginningOrder"]
        self.gameStarted = loadingGame["gameStarted"]
        playerList = []
        for players in loadingGame["playerList"]:
            playerList.append(player.Player(sockets[players], getPlayerData.getPlayerData(players)))
        self.playerList = playerList


if __name__ == "__main__":
    game = Game(10, [player.Player(1234, getPlayerData.getPlayerData("test1@test.com")),
                     player.Player(1235, getPlayerData.getPlayerData("test2@test.com"))])
    game.startGame()
    game.saveData()
