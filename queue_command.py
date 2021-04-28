# queue.py
# By: BentoBot02
# karuta catalog queue command

import discord
import os
from discord.ext import commands
import asyncio
from copy import deepcopy

import globalValues

async def queue(ctx, args):

    if len(args) > 0:
        id = args[0].replace('<', '').replace('@', '').replace('!', '').replace('>', '')
        try:
            id = int(id)
            if globalValues.catalog.getUser(id) == None:
                raise ValueError
        except ValueError:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user was not found.")
            return
    else:
        id = ctx.author.id

    cardCollection = await globalValues.catalog.getUser(id).getQueue()
    cardCollection = deepcopy(cardCollection)

    if len(cardCollection) == 0:
        embedVar = discord.Embed(title="Queued Cards", description="Showing cards carried by <@" + str(id) + ">\n\nThe list is empty.", color=0x6280D1)
        await ctx.channel.send(embed=embedVar)
        return

    cardList = []
    for card in cardCollection.values():
        cardList.append(card)

    cardStrList = []
    for card in cardList:
        cardStrList.append(card.getLookupStr())

    startIndex = 0
    endIndex = startIndex + 10
    if endIndex > len(cardList):
        endIndex = len(cardList)

    cardStr = ""
    for i in range(startIndex, endIndex):
        cardStr += cardStrList[i] + "\n"
    cardStr = cardStr.strip()

    fieldName = "Showing cards " + str(startIndex + 1) + "-"  + str(endIndex) + " of " + str(len(cardList))

    embedVar = discord.Embed(title="Queued Cards", description="Showing cards carried by <@" + str(id) + ">", color=0x6280D1)
    embedVar.add_field(name=fieldName, value=cardStr)
    message = await ctx.channel.send(embed=embedVar)

    if len(cardList) > 10:

        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(react, user):
            return react.message == message and user == ctx.author and (react.emoji == '⬅️' or react.emoji == '➡️')

        while True:
            try:
                reaction = await globalValues.bot.wait_for('reaction_add', timeout=30, check=check)
                reaction = reaction[0].emoji

                if reaction == '⬅️':
                    startIndex -= 10
                    if startIndex < 0:
                        startIndex = 0
                    endIndex = startIndex + 10
                    if endIndex > len(cardStrList):
                        endIndex = len(cardStrList)

                else:
                    endIndex += 10
                    if endIndex > len(cardStrList):
                        endIndex = len(cardStrList)
                    startIndex = endIndex - 10
                    if startIndex < 0:
                        startIndex = 0

                cardStr = ""
                for i in range(startIndex, endIndex):
                    cardStr += cardStrList[i] + "\n"
                cardStr = cardStr.strip()

                fieldName = "Showing cards " + str(startIndex + 1) + "-"  + str(endIndex) + " of " + str(len(cardList))

                embedVar = discord.Embed(title="Queued Cards", description="Showing cards carried by <@" + str(id) + ">", color=0x6280D1)
                embedVar.add_field(name=fieldName, value=cardStr)
                await message.edit(embed=embedVar)

            except asyncio.TimeoutError:
                return

