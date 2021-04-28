# ViewableCatalogClass.py
# By: BentoBot02
# holds the ViewableCatalog class

import os
import aiorwlock
import urllib.request
from urllib.request import urlopen
from PIL import Image
import pickle
import time

from PageClass import Page

CARD_COORDINATES = [(15, 20),
                    (315, 20),
                    (615, 20),
                    (915, 20),
                    (1215, 20),
                    (15, 490),
                    (315, 490),
                    (615, 490),
                    (915, 490),
                    (1215, 490)]

class ViewableCatalog:
    def __init__(self, numPages, cardsPerPage, cloud, header, liveCatalog={}):
        self.liveCatalog = liveCatalog
        self.numPages = numPages
        self.cardsPerPage = cardsPerPage
        self.pages = []
        self.cloud = cloud
        self.header = header
        self.refundList = []

        ticketList = []
        coinList = []

        for card in liveCatalog.values():
            if card.getCurrencyType() == '🎫':
                ticketList.append(card)
            else:
                coinList.append(card)
        
        if len(coinList) > 1:
            coinList = sorted(coinList, key=lambda x : x.getCurrencyAmount(), reverse=True)
        if len(ticketList) > 1:
            ticketList = sorted(ticketList, key=lambda x : x.getCurrencyAmount(), reverse=True)

        fullList = []
        self.refundList = []
        if len(coinList) > self.cardsPerPage:
            fullList = coinList[:self.cardsPerPage]
            refundList = coinList[self.cardsPerPage:]
        else:
            fullList = coinList
        fullList.extend(ticketList)

        self.pages = []
        for pageIndex in range(0, self.numPages):
           
            page = Page(pageIndex, self.cardsPerPage)
            req = urllib.request.Request(self.cloud.getCloudfrontURL() + "general/page_" + str(pageIndex) + ".jpg", headers=self.header)
            backgroundImage = Image.open(urlopen(req))
            backgroundImage.convert('RGBA')
            image = backgroundImage.copy()
            imageFileName = "catalog_page_" + str(pageIndex) + "_v" + str(time.time()) + ".jpg"

            for cardIndex in range(0, self.cardsPerPage):
                if (pageIndex * self.cardsPerPage + cardIndex) < len(fullList):
                    cardFileName = fullList[pageIndex * self.cardsPerPage + cardIndex].getImage()
                    req = urllib.request.Request(self.cloud.getCloudfrontURL() + "cards/" + cardFileName, headers=self.header)
                    cardImage = Image.open(urlopen(req))
                    cardImage.convert('RGBA')
                    image.paste(cardImage, (CARD_COORDINATES[cardIndex][0], CARD_COORDINATES[cardIndex][1]), cardImage)
                    page.addCard(fullList[pageIndex * self.cardsPerPage + cardIndex])
                else:
                    req = urllib.request.Request(self.cloud.getCloudfrontURL() + "general/empty_slot.png", headers=self.header)
                    cardImage = Image.open(urlopen(req))
                    cardImage.convert('RGBA')
                    image.paste(cardImage, (CARD_COORDINATES[cardIndex][0], CARD_COORDINATES[cardIndex][1]), cardImage)

            image.save(imageFileName, quality=95)
            self.cloud.addPublicFile("live-catalog", imageFileName)
            page.setImage(imageFileName, self.cloud.getCloudfrontURL() + "live-catalog/" + imageFileName)
            os.remove(imageFileName)
            page.setPageStr()
            self.pages.append(page)

    # viewable catalog getters

    def getPages(self):
        return self.pages

    def getNumPages(self):
        return self.numPages

    def getCardsPerPage(self):
        return self.cardsPerPage

    def getRefundList(self):
        return self.refundList

    # viewable catalog setters

    def setLiveCatalog(self, liveCatalog):
        self.liveCatalog = liveCatalog

    def setPages(self):
        ticketList = []
        coinList = []

        for card in self.liveCatalog.values():
            if card.getCurrencyType() == '🎫':
                ticketList.append(card)
            else:
                coinList.append(card)
        
        if len(coinList) > 1:
            coinList = sorted(coinList, key=lambda x : x.getCurrencyAmount(), reverse=True)
        if len(ticketList) > 1:
            ticketList = sorted(ticketList, key=lambda x : x.getCurrencyAmount(), reverse=True)

        fullList = []
        if len(coinList) > self.cardsPerPage:
            fullList = coinList[:self.cardsPerPage]
            self.refundList = coinList[self.cardsPerPage:]
        else:
            fullList = coinList
        fullList.extend(ticketList)

        self.pages = []
        for pageIndex in range(0, self.numPages):
           
            page = Page(pageIndex, self.cardsPerPage)
            req = urllib.request.Request(self.cloud.getCloudfrontURL() + "general/page_" + str(pageIndex) + ".jpg", headers=self.header)
            backgroundImage = Image.open(urlopen(req))
            backgroundImage.convert('RGBA')
            image = backgroundImage.copy()
            imageFileName = "catalog_page_" + str(pageIndex) + "_v" + str(time.time()) + ".jpg"

            for cardIndex in range(0, self.cardsPerPage):
                if (pageIndex * self.cardsPerPage + cardIndex) < len(fullList):
                    cardFileName = fullList[pageIndex * self.cardsPerPage + cardIndex].getImage()
                    req = urllib.request.Request(self.cloud.getCloudfrontURL() + "cards/" + cardFileName, headers=self.header)
                    cardImage = Image.open(urlopen(req))
                    cardImage.convert('RGBA')
                    image.paste(cardImage, (CARD_COORDINATES[cardIndex][0], CARD_COORDINATES[cardIndex][1]), cardImage)
                    page.addCard(fullList[pageIndex * self.cardsPerPage + cardIndex])
                else:
                    req = urllib.request.Request(self.cloud.getCloudfrontURL() + "general/empty_slot.png", headers=self.header)
                    cardImage = Image.open(urlopen(req))
                    cardImage.convert('RGBA')
                    image.paste(cardImage, (CARD_COORDINATES[cardIndex][0], CARD_COORDINATES[cardIndex][1]), cardImage)

            image.save(imageFileName, quality=95)
            self.cloud.addPublicFile("live-catalog", imageFileName)
            page.setImage(imageFileName, self.cloud.getCloudfrontURL() + "live-catalog/" + imageFileName)
            os.remove(imageFileName)
            page.setPageStr()
            self.pages.append(page)

    # viewable catalog functions

    def addPage(self, page):
        self.pages.append(page)
        
    def populatePages(self):

        userList = []
        with open("users.txt", "rb") as f:
            try:
                userList = pickle.load(f)
            except EOFError:
                userList = []
        for user in userList:
            newUser = CatalogUser(user[0], user[1][0], user[1][1], user[2])
            self.users[user[0]] = newUser

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

        self.catalogLock = aiorwlock.RWLock()

    def getPageStr(self, index):
        return self.pages[index].getPageStr()

    def getPageImage(self, index):
        return self.pages[index].getImage()

    def getPageImageURL(self, index):
        return self.pages[index].getImageURL()