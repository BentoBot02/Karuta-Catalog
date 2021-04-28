# PageClass.py
# By: BentoBot02
# contains the page class for KarutaCatalog



class Page:
    def __init__(self, pageNum, numCards):
        self.pageNum = pageNum
        self.numCards = numCards
        self.image = ""
        self.imageURL = ""
        self.cards = []
        self.pageStr = ""

    # Page getters

    def getPageNum(self):
        return self.pageNum

    def getNumCards(self):
        return self.numCards

    def getImage(self):
        return self.image

    def getImageURL(self):
        return self.imageURL

    def getCards(self):
        return self.cards

    def getPageStr(self):
        return self.pageStr

    # Page setters

    def setPageNum(self, pageNum):
        self.pageNum = pageNum

    def setNumCards(self, numCards):
        self.numCards = numCards

    def setImage(self, image, imageURL):
        self.image = image
        self.imageURL = imageURL

    def setCards(self, cards):
        self.cards = cards

    # Page functions

    def addCard(self, card):
        self.cards.append(card)

    def setPageStr(self):
        newPageStr = ""
        cardIndex = 0
        while cardIndex < self.numCards:
            if cardIndex < len(self.cards):
                newPageStr += self.cards[cardIndex].getCurrencyType() + " **" + str(self.pageNum * self.numCards + cardIndex + 1) + "** · `" + self.cards[cardIndex].getCode() + "` by <@" + str(self.cards[cardIndex].getID()) + ">\n"
            else:
                newPageStr += "▫️ " + " **" + str(self.pageNum * self.numCards + cardIndex + 1) + "** `Empty Slot`\n"
            cardIndex += 1
        self.pageStr = newPageStr.strip()