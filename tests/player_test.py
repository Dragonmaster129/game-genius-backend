from src.objects import player


class TestPlayer(player.Player):
    def __init__(self, playerData):
        super().__init__(None, playerData)
        self.message = ""
        self.saved = False

    def sendMsg(self, message):
        self.message = message
        self.saved = False

    def saveData(self, collection=None):
        self.saved = True

    def returnMsg(self):
        return self.message
