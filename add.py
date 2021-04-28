# add.py
# By: BentoBot02
# karuta catalog add command

import discord
import os
from discord.ext import commands
import asyncio
import aiorwlock
import urllib.request
from urllib.request import urlopen
from PIL import Image
import time
import random

from CardClass import Card

import globalValues

SERVER_ID = PRIVATE
KARUTA_ID = 646937666251915264
HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

async def add(ctx, args):

    if len(args) < 1:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, please input a card code.")
        return

    code = args[0]
    code = code.lower()

    if await globalValues.catalog.getNextCatalogCard(code) != None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, `" + code + "` is already in queue for the next catalog.")
        return

    guild = globalValues.bot.get_guild(SERVER_ID)
    if guild.get_member(ctx.author.id) == None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, Please check your DM.")
        dm = await ctx.author.create_dm()
        await dm.send("You must join this server to add cards to the catalog. This will ensure buyers can DM you and not just see a Discord ID.\nhttps://discord.gg/PRIVATE")
        return

    tickets = await globalValues.catalog.getTickets(ctx.author.id)
    coins = await globalValues.catalog.getCoins(ctx.author.id)

    if tickets == 0 and coins == 0:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have any coins or tickets.")
        return

    gottenCard = await getCard(ctx, code)
    if gottenCard == None:
        return

    info = gottenCard[0]
    id = gottenCard[1]
    image = gottenCard[2]

    payment = await getPreferredPayment(ctx)
    if payment == None:
        return

    currency = await getCurrency(ctx, tickets, coins)
    if currency == None:
        return

    card = Card(info[0], info[1], info[2], info[3], info[4], info[5], id, image, globalValues.catalog.getCloudfrontURL() + "cards/" + image, payment, currency[0], currency[1])
    confirm = await confirmAdd(ctx, card)

    if confirm:
        success = await globalValues.catalog.setCard(card)

        if not success and card.getCurrencyType() == '🎫':
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough tickets to add `" + code + "` to the catolog.")
        elif not success:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough coins to add `" + code + "` to the catolog.")


##############################################################################################################################################

async def getCard(ctx, code):

    def checkCard(m):
        if m.channel == ctx.channel and m.author.id == KARUTA_ID and m.embeds and m.embeds[0].title == "Card Details" and "<@" + str(ctx.author.id) + ">" in m.embeds[0].description:
            codeStr = m.embeds[0].description.split("**`")[1]
            codeStr = codeStr.split("`**")[0]
            codeStr = codeStr.strip()
            if codeStr == code:
                return True
        return False

    await ctx.channel.send(embed=discord.Embed(title="Input Card", description="Please `k!v` the card you want to add.", color=0x6280D1))

    try:
        message = await globalValues.bot.wait_for('message', timeout=60, check=checkCard)

        text = message.embeds[0].description
        textSplit = text.split('\n')

        ownerStr = textSplit[0]
        ownerStr = ownerStr.split('<@')[1]
        ownerID = ownerStr.replace('!', '').replace('>', '')
        ownerID = int(ownerID)
        
        cardStr = textSplit[2]
        cardInfo = cardStr.split(' · ')
        
        cardCode = cardInfo[0].strip('**').strip('`')
        cardQuality = cardInfo[1].count('★')
        cardPrint = int(cardInfo[2].strip('`').strip('#'))
        cardEdition = int(cardInfo[3].strip('`').strip('◈'))
        cardSeries = cardInfo[4].strip('~~')
        cardCharacter = cardInfo[5].strip('~~').strip('**').replace('\xa0\xa0', ' ')

        cardInfo = [cardCode, cardQuality, cardPrint, cardEdition, cardSeries, cardCharacter]

        url = message.embeds[0].image.url
        req = urllib.request.Request(url, headers=HEADER)
        cardImage = Image.open(urlopen(req))
        cardImage.convert('RGBA')
        cardFileName = code + ".png"
        cardImage.save(cardFileName, quality=95)
        globalValues.catalog.addPublicFile("cards", cardFileName);
        os.remove(cardFileName);

        return [cardInfo, ownerID, cardFileName]
    
    except asyncio.TimeoutError:
        return None

##############################################################################################################################################

async def getPreferredPayment(ctx):
        
    embedVar = discord.Embed(title="**Select Preferred Payment**", description="💵 : `money`\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0🎴 : `cards`\n"
                                                                                         "💎 : `gems`\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0⛏️ : `bits`\n"
                                                                                         "🎟️ : `tickets`\xa0\xa0\xa0\xa0\xa0\xa0\xa0🖼️ : `frames`\n"
                                                                                         "💰 : `gold`\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0❓ : `other`\n\n" +
                                                                                         "✅ : Done Selecting",
                                color=0x6280D1)
    message = await ctx.channel.send(embed=embedVar)
    await message.add_reaction('💵')
    await message.add_reaction('💎')
    await message.add_reaction('🎟️')
    await message.add_reaction('💰')
    await message.add_reaction('🎴')
    await message.add_reaction('⛏️')
    await message.add_reaction('🖼️')
    await message.add_reaction('❓')
    await message.add_reaction('✅')

    def paymentCheck(react, user):
        return react.message == message and user == ctx.author and react.emoji == '✅'

    try:
        await globalValues.bot.wait_for('reaction_add', timeout=60, check=paymentCheck)

        message = await ctx.fetch_message(message.id)

        payments = []

        reactionList = message.reactions
        for reaction in reactionList:
            if reaction.emoji == '💵':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('💵')

            elif reaction.emoji == '💎':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('💎')

            elif reaction.emoji == '🎟️':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('🎟️')

            elif reaction.emoji == '💰':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('💰')

            elif reaction.emoji == '🎴':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('🎴')

            elif reaction.emoji == '⛏️':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('⛏️')

            elif reaction.emoji == '🖼️':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('🖼️')

            elif reaction.emoji == '❓':
                users = await reaction.users().flatten()
                if ctx.author in users:
                    payments.append('❓')
        
        if len(payments) == 0:
            payments.append('❓')

        return payments

    except asyncio.TimeoutError:
        return None

##############################################################################################################################################

async def getCurrency(ctx, tickets, coins):

    def currencyCheck(m):
        return m.channel == ctx.channel and m.author == ctx.author

    embedVar = discord.Embed(title="Input Catalog Payment", description="🪙 · `coin`: bid for the front page\n🎫 · `ticket`: add to the catalog and bid for pages 2-10\n\nFormat: `<amount>` `<currency>`\n\n*Coins and tickets are not Karuta currency.*", color=0x6280D1)
    embedVar.set_footer(text="Highest coin bid: " + str(globalValues.catalog.getHighestCoinBid()) + "\nHighest ticket bid: " + str(globalValues.catalog.getHighestTicketBid()))

    await ctx.channel.send(embed=embedVar)

    while True:
        try:
            message = await globalValues.bot.wait_for('message', timeout=60, check=currencyCheck)

            valid = True
            message = message.content.strip()
            message = message.split()
            if len(message) >= 2:
                try:
                    amount = message[0].replace(',', '')
                    currency = message[1].lower()
                    if currency == "ticket" or currency == "tickets" or currency == "t" or currency == "tix" or currency == '🎫':
                        currency = "🎫"
                    elif currency == "coin" or currency == "coins" or currency == "c" or currency == '🪙':
                        currency = "🪙"
                    else:
                        raise ValueError
                    amount = int(amount)
                    if amount <= 0:
                        await ctx.channel.send("<@" + str(ctx.author.id) + ">, input an amount greater than 0.")
                        valid = False
                except ValueError:
                    valid = False
            
                if valid:
                    if currency == '🎫':
                        if tickets < amount:
                            if tickets == 1:
                                await ctx.channel.send("<@" + str(ctx.author.id) + ">, you have `" + str(tickets) + " ticket`.")
                            else:
                                await ctx.channel.send("<@" + str(ctx.author.id) + ">, you have `" + str(tickets) + " tickets`.")
                            valid = False
                    elif currency == '🪙':
                        if coins < amount:
                            if coins != 1:
                                await ctx.channel.send("<@" + str(ctx.author.id) + ">, you have `" + str(coins) + " coins`.")
                            else:
                                await ctx.channel.send("<@" + str(ctx.author.id) + ">, you have `" + str(coins) + " coin`.")
                            valid = False
                if valid:
                    return [currency, amount]

        except asyncio.TimeoutError:
            return None

##############################################################################################################################################

async def confirmAdd(ctx, card):

    descriptionStr = ""
    descriptionStr += "Owner: <@" + str(card.getID()) + ">\n"
    descriptionStr += "Card Code: `" + card.getCode() + "`\n"
    paymentStr = card.getPaymentStr()
    descriptionStr += "Preferred Payment:\n" + paymentStr + "\n"
    currencyStr = "**" + str(card.getCurrencyAmount()) + "** · "
    if card.getCurrencyType() == '🎫':
        currencyStr += "🎫 · `ticket"
    else:
        currencyStr += "🪙 · `coin"
    if card.getCurrencyAmount() != 1:
        currencyStr += "s"
    currencyStr += "`"
    descriptionStr += "Catalog Payment:\n" + currencyStr

    embedVar = discord.Embed(title="Confirm Addition", description=descriptionStr, color=0x6280D1)

    message = await ctx.channel.send(embed=embedVar)
    await message.add_reaction('❌')
    await message.add_reaction('✅')

    def confirmCheck(react, user):
        return react.message == message and user == ctx.author and (react.emoji == '❌' or react.emoji == '✅')

    try:
        reaction = await globalValues.bot.wait_for('reaction_add', timeout=60, check=confirmCheck)
        reaction = reaction[0].emoji

        if reaction == '✅':
            await message.edit(embed=discord.Embed(title="Confirm Addition", description=descriptionStr, color=discord.Color.green()))
            return True
        else:
            raise asyncio.TimeoutError
    except asyncio.TimeoutError:
        await message.edit(embed=discord.Embed(title="Confirm Addition", description=descriptionStr, color=discord.Color.red()))
        return False