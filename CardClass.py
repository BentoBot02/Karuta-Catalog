# CardClass.py
# By: BentoBot02
# holds the card class

class Card:

    class CardInfo:
        def __init__(self, code, quality, print, edition, series, character):
            self.code = code
            self.quality = quality
            self.print = print
            self.edition = edition
            self.series = series
            self.character = character

        # card info getters

        def getCode(self):
            return self.code

        def getQuality(self):
            return self.quality

        def getPrint(self):
            return self.print

        def getEdition(self):
            return self.edition

        def getSeries(self):
            return self.series

        def getCharacter(self):
            return self.character

        # card info setters

        def setCode(self, code):
            self.code = code

        def setQuantity(self, quantity):
            self.quantity = quantity

        def setPrint(self, print):
            self.print = print

        def setEdition(self, edition):
            self.edition = edition

        def setSeries(self, series):
            self.series = series

        def setCharacter(self, character):
            self.name = character

        # card info functions

        def getQualityStr(self):
            qualityStr = ""
            fullStarCount = 0
            starCount = 0
            while starCount < 4:
                if fullStarCount < self.quality:
                    qualityStr += "★"
                    fullStarCount += 1
                else:
                    qualityStr += "☆"
                starCount += 1
            return qualityStr

    class Currency:
        def __init__(self, type, amount):
            self.type = type
            self.amount = amount

        # getters

        def getType(self):
            return self.type

        def getAmount(self):
            return self.amount

        # setters

        def setType(self, type):
            self.type = type

        def setAmount(self, amount):
            self.amount = amount

    def __init__(self, code="", quality=0, print=0, edition=0, series="", character="", id=0, image="", imageURL="", payment=[], currencyType='', currencyAmount=0):
        self.info = self.CardInfo(code, quality, print, edition, series, character)
        self.id = id
        self.image = image
        self.imageURL = imageURL
        self.payment = payment
        self.currency = self.Currency(currencyType, currencyAmount)
        self.viewStr = ""
        self.lookupStr = ""
        self.setLookupStr()
        
    # getters

    def getCode(self):
        return self.info.getCode()

    def getQuality(self):
        return self.info.getQuality()

    def getPrint(self):
        return self.info.getPrint()

    def getEdition(self):
        return self.info.getEdition()

    def getSeries(self):
        return self.info.getSeries()

    def getCharacter(self):
        return self.info.getCharacter()

    def getID(self):
        return self.id

    def getImage(self):
        return self.image

    def getImageURL(self):
        return self.imageURL

    def getPayment(self):
        return self.payment

    def getCurrencyType(self):
        return self.currency.getType()

    def getCurrencyAmount(self):
        return self.currency.getAmount()

    def getViewStr(self):
        return self.viewStr

    def getLookupStr(self):
        return self.lookupStr

    # setters

    def setCode(self, code):
        self.info.setCode(code)
        self.setLookupStr()

    def setQuality(self, quality):
        self.info.setQuality(quality)
        self.setLookupStr()

    def setPrint(self, print):
        self.info.setPrint(print)
        self.setLookupStr()

    def setEdition(self, edition):
        self.info.setEdition(edition)
        self.setLookupStr()

    def setSeries(self, series):
        self.info.setSeries(series)
        self.setLookupStr()

    def setCharacter(self, character):
        self.info.setCharacter(character)
        self.setLookupStr()

    def setID(self, id):
        self.id = id

    def setImage(self, image, imageURL):
        self.image = image
        self.imageURL = imageURL

    def setPayment(self, payment):
        self.payment = payment
        self.setLookupStr()

    def setCurrencyType(self, type):
        self.currency.setType(type)
        self.setLookupStr()

    def setCurrencyAmount(self, amount):
        self.currency.setAmount(amount)
        self.setLookupStr()

    def setViewStr(self):
        characterStr = self.info.getCharacter().replace(' ', '\xa0\xa0')
        self.viewStr = "Owned by <@" + str(self.id) + ">\n\n**`" + self.info.getCode() + "`** · `" + self.info.getQualityStr() + "` · `#" + str(self.info.getPrint()) + "` · `◈" + str(self.info.getEdition()) + "` · " + self.info.getSeries() + " · **" + characterStr + "**"

    def setLookupStr(self):
        self.lookupStr = self.payment[0] + " **`" + self.info.getCode() + "`** · `" + str(self.info.getQualityStr()) + "` · `#" + str(self.info.getPrint()) + "` · " + "`◈" + str(self.info.getEdition()) + "` · " + self.info.getSeries() + " · **" + self.info.getCharacter() + "**"
    
    # card functions

    def getPaymentStr(self):
        paymentStr = ""
        for type in self.payment:
            paymentStr += type + " · "
        return paymentStr[:-3]

    def getQualityStr(self):
        return self.info.getQualityStr()