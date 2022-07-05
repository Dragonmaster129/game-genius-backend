class Game:
    def __init__(self, ID, playerList):
        self.id = ID
        self.playerList = playerList
        self.currentTurn = 0
        self.currentAction = "STARTTURN"
        self.actionList = ["STARTTURN", "PAYCHECK", "OPPORTUNITY", "MARKET",
                           "DOODAD", "BABY", "CHARITY", "DOWNSIZED", "ENDTURN"]
        self.currentTarget = 0
        self.gameStarted = False

    def saveData(self, collection):
        # TODO save the data
        pass

    def nextTurn(self):
        self.currentTurn = (self.currentTurn + 1) % len(self.playerList)

    def playerToRightSingle(self):
        self.currentTarget = (self.currentTurn - 1) % len(self.playerList)

    def sendMsgToAllPlayers(self, msg):
        for player in self.playerList:
            player.sendMsg(msg)

    def addPlayer(self, player):
        if not self.gameStarted:
            self.playerList.append(player)

    def getPlayerList(self):
        return self.playerList

    def getCurrentTarget(self):
        return self.currentTarget

    def getCurrentPlayer(self):
        return self.currentTurn
