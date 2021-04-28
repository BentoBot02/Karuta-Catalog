# CooldownClass.py
# By: BentoBot02
# holds the Cooldown class

import time

class Cooldown:
    def __init__(self, serverVote, botVote):
        self.serverVote = serverVote
        self.botVote = botVote

    # getters

    def getServerVote(self):
        return self.serverVote

    def getBotVote(self):
        return self.botVote

    # setters

    def setServerVote(self, serverVote):
        self.serverVote = serverVote

    def setBotVote(self, botVote):
        self.botVote = botVote

    # cooldown functions

    def getServerVoteDiff(self):
        now = time.time()
        diff = now - self.serverVote
        return diff

    def getBotVoteDiff(self):
        now = time.time()
        diff = now - self.botVote
        return diff

    def getServerVoteStr(self):
        now = time.time()
        diff = 43200 - (now - self.serverVote)
        if diff <= 0:
            return "**Server Vote** is currently available"
        elif diff >= 3600:
            diff = round(diff / 3600)
            if diff != 1:
                return "**Server Vote** is available in `" + str(diff) + " hours`"
            else:
                return "**Server Vote** is available in `" + str(diff) + "hour`"
        elif diff >= 60:
            diff = round(diff / 60)
            if diff != 1:
                return "**Server Vote** is available in `" + str(diff) + " minutes`"
            else:
                return "**Server Vote** is available in `" + str(diff) + "minute`"
        else:
            if diff != 1:
                return "**Server Vote** is available in `" + str(diff) + " seconds`"
            else:
                return "**Server Vote** is available in `" + str(diff) + "second`"

    def getBotVoteStr(self):
        now = time.time()
        diff = 43200 - (now - self.botVote)
        if diff <= 0:
            return "**Bot Vote** is currently available"
        elif diff >= 3600:
            diff = round(diff / 3600)
            if diff != 1:
                return "**Bot Vote** is available in `" + str(diff) + " hours`"
            else:
                return "**Bot Vote** is available in `" + str(diff) + "hour`"
        elif diff >= 60:
            diff = round(diff / 60)
            if diff != 1:
                return "**Bot Vote** is available in `" + str(diff) + " minutes`"
            else:
                return "**Bot Vote** is available in `" + str(diff) + "minute`"
        else:
            if diff != 1:
                return "**Bot Vote** is available in `" + str(diff) + " seconds`"
            else:
                return "**Bot Vote** is available in `" + str(diff) + "second`"