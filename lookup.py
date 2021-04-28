# lookup.py
# By: BentoBot02
# karuta catalog lookup command

import discord
import os
from discord.ext import commands
import asyncio
from copy import deepcopy

import globalValues

async def lookup(ctx, args):

    for arg in args:
        arg = arg.lower()

    validTotalParameters = ["quality", "q", "print", "p", "edition", "e"]
    validTotalOperators = [":", "=", "<=", "<", ">=", ">"]

    validPartialParameters = ["series", "s", "character", "c"]
    validPartialOperators = [":", "="]

    validOperands = []
    for param in validTotalParameters:
        for operator in validTotalOperators:
            validOperands.append(param + operator)

    for param in validPartialParameters:
        for operator in validPartialOperators:
            validOperands.append(param + operator)

    actualArgs = []
    for arg in args:
        if len(actualArgs) == 0:
            actualArgs.append(arg)
        else:
            isOperand = False
            for operand in validOperands:
                if arg.startswith(operand):
                    if arg.startswith("quality"):
                        arg = arg.replace("quality", "q", 1)
                    elif arg.startswith("print"):
                        arg = arg.replace("print", "p", 1)
                    elif arg.startswith("edition"):
                        arg = arg.replace("edition", "e", 1)
                    elif arg.startswith("series"):
                        arg = arg.replace("series", "s", 1)
                    elif arg.startswith("character"):
                        arg = arg.replace("character", "c", 1)
                    actualArgs.append(arg)
                    isOperand = True
                    break
            if not isOperand:
                actualArgs[len(actualArgs) - 1] += " " + arg

    if len(actualArgs) > 0:
        validArgs = False
        for operand in validOperands:
            if actualArgs[0].startswith(operand):
                validArgs = True
                break

        if not validArgs:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, please input a valid parameter.")
            return
    
    #[XXXcard codeXXX, quality, print, edition, series, character]
    #sort: series (ascend), character (ascend), edition (ascend), quality (descend), print (ascend)
    QUALITY_INDEX = 0
    PRINT_INDEX = 1
    EDITION_INDEX = 2
    SERIES_INDEX = 3
    CHARACTER_INDEX = 4
    cardParameters = [['>', -1], ['>', -1], ['>', -1], ['=', ""], ['=', ""]]

    try:
        for arg in actualArgs:
            if arg.startswith('q:') or arg.startswith('q='):
                cardParameters[0][0] = '='
                if len(arg[2:]) == 0:
                    return
                cardParameters[0][1] = int(arg[2:])

            elif arg.startswith('q<='):
                cardParameters[0][0] = '<='
                if len(arg[3:]) == 0:
                    return
                cardParameters[0][1] = int(arg[3:])

            elif arg.startswith('q<'):
                cardParameters[0][0] = '<'
                if len(arg[2:]) == 0:
                    return
                cardParameters[0][1] = int(arg[2:])

            elif arg.startswith('q>='):
                cardParameters[0][0] = '>='
                if len(arg[3:]) == 0:
                    return
                cardParameters[0][1] = int(arg[3:])

            elif arg.startswith('q>'):
                cardParameters[0][0] = '>'
                if len(arg[2:]) == 0:
                    return
                cardParameters[0][1] = int(arg[2:])

            elif arg.startswith('p:') or arg.startswith('p='):
                cardParameters[1][0] = '='
                if len(arg[2:]) == 0:
                    return
                cardParameters[1][1] = int(arg[2:])

            elif arg.startswith('p<='):
                cardParameters[1][0] = '<='
                if len(arg[3:]) == 0:
                    return
                cardParameters[1][1] = int(arg[3:])

            elif arg.startswith('p<'):
                cardParameters[1][0] = '<'
                if len(arg[2:]) == 0:
                    return
                cardParameters[1][1] = int(arg[2:])

            elif arg.startswith('p>='):
                cardParameters[1][0] = '>='
                if len(arg[3:]) == 0:
                    return
                cardParameters[1][1] = int(arg[3:])

            elif arg.startswith('p>'):
                cardParameters[1][0] = '>'
                if len(arg[2:]) == 0:
                    return
                cardParameters[1][1] = int(arg[2:])

            elif arg.startswith('e:') or arg.startswith('e='):
                cardParameters[2][0] = '='
                cardParameters[2][1] = int(arg[2:])

            elif arg.startswith('e<='):
                cardParameters[2][0] = '<='
                if len(arg[3:]) == 0:
                    return
                cardParameters[2][1] = int(arg[3:])

            elif arg.startswith('e<'):
                cardParameters[2][0] = '<'
                if len(arg[2:]) == 0:
                    return
                cardParameters[2][1] = int(arg[2:])

            elif arg.startswith('e>='):
                cardParameters[2][0] = '>='
                if len(arg[3:]) == 0:
                    return
                cardParameters[2][1] = int(arg[3:])

            elif arg.startswith('e>'):
                cardParameters[2][0] = '>'
                if len(arg[2:]) == 0:
                    return
                cardParameters[2][1] = int(arg[2:])

            elif arg.startswith('s:') or arg.startswith('s='):
                cardParameters[3][0] = '='
                if len(arg[2:]) == 0:
                    return
                cardParameters[3][1] = arg[2:]

            elif arg.startswith('c:') or arg.startswith('c='):
                cardParameters[4][0] = '='
                if len(arg[3:]) == 0:
                    return
                cardParameters[4][1] = arg[2:]

    except ValueError:
        return

    cardList = []

    fullLiveCatalog = deepcopy(globalValues.catalog.getLiveCatalog())

    for info in fullLiveCatalog.values():
        addCard = True
        if addCard:
            if cardParameters[QUALITY_INDEX][0] == '=':
                if not (info.getQuality() == cardParameters[QUALITY_INDEX][1]):
                    addCard = False
            elif cardParameters[QUALITY_INDEX][0] == '<=':
                if not (info.getQuality() <= cardParameters[QUALITY_INDEX][1]):
                    addCard = False
            elif cardParameters[QUALITY_INDEX][0] == '<':
                if not (info.getQuality() < cardParameters[QUALITY_INDEX][1]):
                    addCard = False
            elif cardParameters[QUALITY_INDEX][0] == '>=':
                if not (info.getQuality() >= cardParameters[QUALITY_INDEX][1]):
                    addCard = False
            elif cardParameters[QUALITY_INDEX][0] == '>':
                if not (info.getQuality() > cardParameters[QUALITY_INDEX][1]):
                    addCard = False
        
        if addCard:
            if cardParameters[PRINT_INDEX][0] == '=':
                if not (info.getPrint() == cardParameters[PRINT_INDEX][1]):
                    addCard = False
            elif cardParameters[PRINT_INDEX][0] == '<=':
                if not (info.getPrint() <= cardParameters[PRINT_INDEX][1]):
                    addCard = False
            elif cardParameters[PRINT_INDEX][0] == '<':
                if not (info.getPrint() < cardParameters[PRINT_INDEX][1]):
                    addCard = False
            elif cardParameters[PRINT_INDEX][0] == '>=':
                if not (info.getPrint() >= cardParameters[PRINT_INDEX][1]):
                    addCard = False
            elif cardParameters[PRINT_INDEX][0] == '>':
                if not (info.getPrint() > cardParameters[PRINT_INDEX][1]):
                    addCard = False

        if addCard:
            if cardParameters[EDITION_INDEX][0] == '=':
                if not (info.getEdition() == cardParameters[EDITION_INDEX][1]):
                    addCard = False
            elif cardParameters[EDITION_INDEX][0] == '<=':
                if not (info.getEdition() <= cardParameters[EDITION_INDEX][1]):
                    addCard = False
            elif cardParameters[EDITION_INDEX][0] == '<':
                if not (info.getEdition() < cardParameters[EDITION_INDEX][1]):
                    addCard = False
            elif cardParameters[EDITION_INDEX][0] == '>=':
                if not (info.getEdition() >= cardParameters[EDITION_INDEX][1]):
                    addCard = False
            elif cardParameters[EDITION_INDEX][0] == '>':
                if not (info.getEdition() > cardParameters[EDITION_INDEX][1]):
                    addCard = False

        if addCard:
            if not cardParameters[SERIES_INDEX][1] in info.getSeries().lower():
                addCard = False

        if addCard:
            if not cardParameters[CHARACTER_INDEX][1] in info.getCharacter().lower():
                addCard = False

        if addCard:
            cardList.append(info)

    if len(cardList) > 0:
        cardList = sorted(cardList, key=lambda x: (x.getSeries(), x.getCharacter(), x.getEdition(), -x.getQuality(), x.getPrint()))

    if len(cardList) == 0:
        embedVar = discord.Embed(title="Catalog Results", description="The list is empty.", color=0x6280D1)
        await ctx.channel.send(embed=embedVar)
        return

    cardStrList = []
    for card in cardList:
        cardStrList.append(card.getLookupStr())

    startIndex = 0
    endIndex = startIndex + 10
    if endIndex > len(cardStrList):
        endIndex = len(cardStrList)

    resultStr = ""
    for i in range(startIndex, endIndex):
        resultStr += cardStrList[i] + "\n"

    fieldName = "Showing results " + str(startIndex + 1) + "-"  + str(endIndex) + " of " + str(len(cardStrList))

    embedVar = discord.Embed(title="Catalog Results", color=0x6280D1)
    embedVar.add_field(name=fieldName, value=resultStr)

    message = await ctx.channel.send(embed=embedVar)

    if len(cardList) > 10:

        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def lookupCheck(react, user):
            return react.message == message and user == ctx.author and (react.emoji == '⬅️' or react.emoji == '➡️')

        while True:
            try:
                reaction = await globalValues.bot.wait_for('reaction_add', timeout=30, check=lookupCheck)
                reaction = reaction[0].emoji

                if reaction == '⬅️':
                    startIndex -= 10
                    if startIndex < 0:
                        startIndex = 0
                    endIndex = startIndex + 10
                    if endIndex > len(cardList):
                        endIndex = len(cardList)
                else:
                    endIndex += 10
                    if endIndex > len(cardList):
                        endIndex = len(cardList)
                    startIndex = endIndex - 10
                    if startIndex < 0:
                        startIndex = 0

                resultStr = ""
                for i in range(startIndex, endIndex):
                    resultStr += cardStrList[i] + "\n"

                fieldName = "Showing results " + str(startIndex + 1) + "-"  + str(endIndex) + " of " + str(len(cardList))
                    
                embedVar.set_field_at(0, name=fieldName, value=resultStr)
                await message.edit(embed=embedVar)

            except asyncio.TimeoutError:
                return