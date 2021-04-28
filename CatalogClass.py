# CatalogClass.py
# By: BentoBot02
# holds the Catalog class

import discord
import os
import boto3
import aiorwlock
import urllib.request
from urllib.request import urlopen
from PIL import Image
import pickle
import time

from CardClass import Card
from CloudClass import Cloud
from CatalogUserClass import CatalogUser
from ViewableCatalogClass import ViewableCatalog
from CooldownClass import Cooldown


class Catalog:
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, CLOUDFRONTURL, HEADER, NUM_PAGES, CARDS_PER_PAGE):
        self.cloud = Cloud(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, CLOUDFRONTURL, HEADER)
        self.users = {}
        self.liveCatalog = {}
        self.nextCatalog = {}
        self.highestTicketCode = ""
        self.highestTicketBid = 0
        self.highestCoinBid = ""
        self.highestCoinBid = 0
        self.catalogLock = aiorwlock.RWLock()

        self.cloud.getFile("general", "users.txt")
        self.cloud.getFile("general", "liveCatalog.txt")
        self.cloud.getFile("general", "nextCatalog.txt")

        userList = []
        with open("users.txt", "rb") as f:
            try:
                userList = pickle.load(f)
            except EOFError:
                userList = []

        for user in userList:
            self.users[user[0]] = CatalogUser(user[0], user[1][0], user[1][1], user[2], user[3], user[4])


        with open("liveCatalog.txt", "rb") as f:
            try:
                self.liveCatalog = pickle.load(f)
            except EOFError:
                self.liveCatalog = {}

        with open("nextCatalog.txt", "rb") as f:
            try:
                self.nextCatalog = pickle.load(f)
            except EOFError:
                self.nextCatalog = {}

        for card in self.nextCatalog.values():
            if card.getCurrencyType() == '🎫' and card.getCurrencyAmount() > self.highestTicketBid:
                self.highestTicketCode = card.getCode()
                self.highestTicketBid = card.getCurrencyAmount()
            elif card.getCurrencyType() == '🪙' and card.getCurrencyAmount() > self.highestCoinBid:
                self.highestCoinCode = card.getCode()
                self.highestCoinBid = card.getCurrencyAmount()

        self.viewableCatalog = ViewableCatalog(NUM_PAGES, CARDS_PER_PAGE, self.cloud, HEADER, self.liveCatalog)

    # catalog getters

    def getUsers(self):
        return self.users

    def getUser(self, id):
        return self.users.get(id)

    async def getTickets(self, id):
        return await self.users.get(id).getTickets()

    async def getCoins(self, id):
        return await self.users.get(id).getCoins()

    def getServerVoteStr(self, id):
        return self.users.get(id).getServerVoteStr()

    def getBotVoteStr(self, id):
        return self.users.get(id).getBotVoteStr()

    def getViewableCatalog(self):
        return self.viewableCatalog

    def getLiveCatalog(self):
        return self.liveCatalog

    def getNextCatalog(self):
        return self.nextCatalog

    def getHighestTicketBid(self):
        return self.highestTicketBid

    def getHighestCoinBid(self):
        return self.highestCoinBid

    def getCloudfrontURL(self):
        return self.cloud.getCloudfrontURL()

    # catalog setters

    async def addTickets(self, id, num):
        if self.users.get(id) == None:
            return False
        else:
            await self.users.get(id).addTickets(num)

    async def addCoins(self, id, num):
        if self.users.get(id) == None:
            return False
        else:
            await self.users.get(id).addCoins(num)

    def setServerVote(self, id):
        now = time.time()
        self.users.get(id).setServerVote(now)

    def setBotVote(self, id):
        now = time.time()
        self.users.get(id).setBotVote(now)

    def setInventories(self, inventories):
        self.inventories = inventories

    def setViewableCatalog(self, viewableCatalog):
        self.viewableCatalog = viewableCatalog

    def setLiveCatalog(self, liveCatalog):
        self.liveCatalog = liveCatalog

    def setNextCatalog(self, nextCatalog):
        self.nextCatalog = nextCatalog

    def setHighestTicketBid(self, bid):
        self.highestTicketBid = bid

    def setHighestCoinBid(self, bid):
        self.highestCoinBid = bid

    # catalog functions

    # add a user
    def addUser(self, user):
        self.users[user.getID()] = user

    # get a card in the next catalog
    async def getNextCatalogCard(self, code):
        async with self.catalogLock.reader_lock:
            return self.nextCatalog.get(code)

    # get a card in the live catalog
    async def getLiveCatalogCard(self, code):
        async with self.catalogLock.reader_lock:
            return self.liveCatalog.get(code)

    # set a card in next catalog
    async def setCard(self, card):
        async with self.catalogLock.writer_lock:
            if self.users.get(card.getID()) != None:
                if card.getCurrencyType() == '🎫' and await self.users.get(card.getID()).subTickets(card.getCurrencyAmount()):
                    if card.getCurrencyAmount() > self.highestTicketBid:
                        self.highestTicketCode = card.getCode()
                        self.highestTicketBid = card.getCurrencyAmount()
                elif card.getCurrencyType() == '🪙' and await self.users.get(card.getID()).subCoins(card.getCurrencyAmount()):
                    if card.getCurrencyAmount() > self.highestCoinBid:
                        self.highestCoinCode = card.getCode()
                        self.highestCoinBid = card.getCurrencyAmount()
                else:
                    return False
                self.nextCatalog[card.getCode()] = card
                await self.users.get(card.getID()).setCard(card)
                return True
            else:
                return False

    # edit a card in next catalog
    async def editCard(self, code, payment, currency):
        async with self.catalogLock.writer_lock:
            card = await self.getNextCatalogCard(code)
            if card != None:
                origType = card.getCurrencyType()
                origPrice = card.getCurrencyAmount()
                if origType == currency[0]:
                    diff = origPrice - currency[1]
                    if diff < 0 and currency[0] == '🎫':
                        sub = await self.users.get(card.getID()).subTickets(diff)
                        if not sub:
                            return False
                    elif currency[0] == '🎫':
                        await self.users.get(card.getID()).addTickets(diff)
                    elif diff < 0:
                        sub = await self.users.get(card.getID()).subCoins(diff)
                        if not sub:
                            return False
                    else:
                        await self.users.get(card.getID()).addCoins(diff)
                else:
                    if currency[0] == '🎫':
                        sub = await self.users.get(card.getID()).subTickets(diff)
                        if not sub:
                            return False
                        await self.users.get(card.getID()).addCoins(origPrice)
                    else:
                        sub = await self.users.get(card.getID()).subCoins(diff)
                        if not sub:
                            return False
                        await self.users.get(card.getID()).addTickets(origPrice)
                card.setPayment(payment)
                card.setCurrencyType(currency[0])
                card.setCurrencyAmount(currency[1])
                self.nextCatalog[card.getCode()] = card
                if self.highestTicketCode == card.getCode() or self.highestCoinBid == card.getCode():
                    maxBid = 0
                    for card in self.nextCatalog.values():
                        if card.getCurrencyType() == '🎫' and card.getCurrencyAmount() > maxBid:
                            self.highestTicketCode = card.getCode()
                            self.highestTicketBid = card.getCurrencyAmount()
                    maxBid = 0
                    for card in self.nextCatalog.values():
                        if card.getCurrencyType() == '🪙' and card.getCurrencyAmount() > maxBid:
                            self.highestCoinCode = card.getCode()
                            self.highestCoinBid = card.getCurrencyAmount()
                elif card.getCurrencyType == '🎫' and self.highestTicketBid < card.getCurrencyAmount():
                    self.highestTicketCode = card.getCode()
                    self.highestTicketBid = card.getCurrencyAmount()
                elif card.getCurrencyType == '🪙' and self.highestCoinBid < card.getCurrencyAmount():
                    self.highestCoinCode = card.getCode()
                    self.highestCoinBid = card.getCurrencyAmount()
                await self.users.get(card.getID()).setCard(card)
        return True


    # pop a card from next catalog
    async def popCard(self, code):
        card = None
        async with self.catalogLock.writer_lock:
            card = self.nextCatalog.pop(code)
        await self.users.get(card.getID()).popCard(card.getCode())
        if card == None:
            return False
        if card.getCurrencyType() == '🎫':
            await self.getUser(card.getID()).addTickets(card.getCurrencyAmount())
        else:
            await self.getUser(card.getID()).addCoins(card.getCurrencyAmount())

        
    # get the given page str
    def getPageStr(self, index):
        return self.viewableCatalog.getPageStr(index)


    # add or subtract currency to a user's inventory
    async def addCurrency(self, id, currencies):
        if currencies[0] != 0:
            await self.users[id].addTickets(currencies[0])
        if currencies[1] != 0:
            await self.users[id].addTickets(currencies[1])

    # implement a trade
    async def trade(self, id0, items0, id1, items1):
        if not await self.users[id0].subTrade(items0):
            return False
        if not await self.users[id1].subTrade(items1):
            self.users[id0].addTrade(items0)
            return False
        await self.users[id0].addTrade(items1)
        await self.users[id1].addTrade(items0)
        return True
            
    # create a new user
    def verify(self, id):
        if self.users.get(id) == None:
            queue = {}
            live = {}
            cooldown = Cooldown(0, 0)
            self.users[id] = CatalogUser(id, 2, 0, queue, live, cooldown)
            return True
        else:
            return False

    # refresh the catalogs
    async def refresh(self):
        async with self.catalogLock.writer_lock:

            self.highestTicketCode = ""
            self.highestTicketBid = 0
            self.highestCoinBid = ""
            self.highestCoinBid = 0

            pages = self.viewableCatalog.getPages()
            for page in pages:
                self.cloud.removeFile("live-catalog", page.getImage())

            for card in self.liveCatalog.values():
                self.cloud.removeFile("cards", card.getImage())

            self.liveCatalog = self.nextCatalog
            for card in self.liveCatalog.values():
                card.setViewStr()
                card.setLookupStr()
            self.nextCatalog = {}

            for user in self.users.values():
                await user.refresh()

            self.viewableCatalog.setLiveCatalog(self.liveCatalog)
            self.viewableCatalog.setPages()

            refundList = self.viewableCatalog.getRefundList()

            for card in refundList:
                await self.users.get(card.getID()).addCoins(card.getCurrencyAmount())
                self.liveCatalog.pop(card.getCode())

        await self.save()

        return (self.viewableCatalog.getPageStr(0), self.viewableCatalog.getPageImageURL(0))

    async def save(self):
        async with self.catalogLock.writer_lock:
            userList = []
            for user in self.users.values():
                userInfo = await user.save()
                userList.append(userInfo)

            with open("users.txt", "wb") as f:
                pickle.dump(userList, f)

            with open("liveCatalog.txt", "wb") as f:
                pickle.dump(self.liveCatalog, f)

            with open("nextCatalog.txt", "wb") as f:
                pickle.dump(self.nextCatalog, f)

            self.cloud.addPrivateFile("general", "users.txt")

            self.cloud.addPrivateFile("general", "liveCatalog.txt")

            self.cloud.addPrivateFile("general", "nextCatalog.txt")

    def addPublicFile(self, folder, fileName):
        self.cloud.addPublicFile(folder, fileName)