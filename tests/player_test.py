from src.objects import player


class TestPlayer(player.Player):
    def __init__(self, playerData):
        super().__init__(None, playerData)
        self.message = ""

    def sendMsg(self, message):
        self.message = message

    def saveData(self, collection):
        pass

    def returnMsg(self):
        return self.message
