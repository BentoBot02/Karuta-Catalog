# CatalogUserClass.py
# By: BentoBot02
# holds the catalog user class

import aiorwlock
import CardClass

from CooldownClass import Cooldown

class CatalogUser():
    class Inventory:
        def __init__(self, tickets, coins):
            self.tickets = tickets
            self.coins = coins
            self.lock = aiorwlock.RWLock()

        # getters

        async def getTickets(self):
            async with self.lock.reader_lock:
                return self.tickets

        async def getCoins(self):
            async with self.lock.reader_lock:
                return self.coins

        def getLock(self):
            return self.lock

        # setters

        def setTickets(self, num):
            self.tickets = num

        def setCoins(self, num):
            self.coins = num

        # functions

        async def addTickets(self, num):
            async with self.lock.writer_lock:
                self.tickets += num

        async def subTickets(self, num):
            async with self.lock.writer_lock:
                if self.tickets < num:
                    return False
                else:
                    self.tickets -= num
                    return True

        async def addCoins(self, num):
            async with self.lock.writer_lock:
                self.coins += num

        async def subCoins(self, num):
            async with self.lock.writer_lock:
                if self.coins < num:
                    return False
                else:
                    self.coins -= num
                    return True

        async def addTrade(self, currencies):
            async with self.lock.writer_lock:
                self.tickets += currencies[0]
                self.coins += currencies[1]

        async def subTrade(self, currencies):
            async with self.lock.writer_lock:
                diffTickets = self.tickets - currencies[0]
                diffCoins = self.coins - currencies[1]
                if diffTickets < 0 or diffCoins < 0:
                    return False
                self.tickets -= currencies[0]
                self.coins -= currencies[1]
                return True


        async def save(self):
            async with self.lock.writer_lock:
                return [self.tickets, self.coins]

    def __init__(self, id, tickets, coins, queue, live, cooldown):
        self.id = id
        self.inventory = self.Inventory(tickets, coins)
        self.queue = queue
        self.live = live
        self.cooldown = cooldown
        self.collectionLock = aiorwlock.RWLock()

    # getters

    def getID(self):
        return self.id

    def getTickets(self):
        return self.inventory.getTickets()

    def getCoins(self):
        return self.inventory.getCoins()

    async def getQueue(self):
        async with self.collectionLock.reader_lock:
            return self.queue

    async def getLive(self):
        async with self.collectionLock.reader_lock:
            return self.live

    def getServerVoteStr(self):
        return self.cooldown.getServerVoteStr()

    def getBotVoteStr(self):
        return self.cooldown.getBotVoteStr()

    # setters

    def setID(self, id):
        self.id = id

    def setTickets(self, tickets):
        self.inventory.setTickets()

    def setCoins(self, coins):
        self.inventory.setCoins()

    async def setQueue(self, cardList):
        async with self.collectionLock:
            self.queue = {}
            for card in cardList:
                self.live[card.getCode()] = card

    async def setLive(self, cardList):
        async with self.collectionLock:
            self.live = {}
            for card in cardList:
                self.live[card.getCode()] = card

    def setServerVote(self, now):
        self.cooldown.setServerVote(now)

    def setBotVote(self, now):
        self.cooldown.setBotVote(now)

    # functions

    async def addTickets(self, num):
        await self.inventory.addTickets(num)
    
    async def addCoins(self, num):
        await self.inventory.addCoins(num)

    async def subTickets(self, num):
        return await self.inventory.subTickets(num)

    async def subCoins(self, num):
        return await self.inventory.subCoins(num)

    async def addTrade(self, currencies):
        return await self.inventory.addTrade(currencies)

    async def subTrade(self, currencies):
        return await self.inventory.subTrade(currencies)

    async def setCard(self, card):
        async with self.collectionLock.writer_lock:
            self.queue[card.getCode()] = card

    async def setCards(self, cardList):
        async with self.collectionLock.writer_lock:
            for card in cardList:
                self.queue[card.getCode()] = card

    async def popCard(self, code):
        async with self.collectionLock.writer_lock:
            self.collection.pop(code)

    async def popCards(self, codes):
        async with self.collectionLock.writer_lock:
            for code in codes:
                self.collection.pop(code)

    async def clearQueue(self):
        async with self.collectionLock.writer_lock:
            self.queue = {}

    async def refresh(self):
        async with self.collectionLock.writer_lock:
            self.live = self.queue
            self.queue = {}

    async def save(self):
        async with self.collectionLock.reader_lock:
            inventory = await self.inventory.save()
            return [self.id, inventory, self.queue, self.live, self.cooldown]