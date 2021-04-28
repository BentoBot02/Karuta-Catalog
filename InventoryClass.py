# InventoryClass.py
# By: BentoBot02
# holds the inventory class

import aiorwlock

class Inventory:
    def __init__(self, id, tickets=0, coins=0):
        self.id = id
        self.tickets = tickets
        self.coins = coins
        self.lock = aiorwlock.RWLock()

    def getID():
        return id

    def getTickets():
        return tickets

    def getCoins():
        return coins

    def getLock():
        return lock

    def setID(id):
        self.id = id

    def setTickets(num):
        self.tickets = num

    def setCoinds(num):
        self.coins = num

    def addTickets(num):
        self.tickets += num

    def addCoins(num):
        self.coins += num

    def save():
        return [self.id, self.tickets, self.coins]