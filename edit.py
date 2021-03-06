# edit.py
# By: PVCPipe01
# karuta catalog edit command

import discord
import os
from discord.ext import commands
import asyncio
import aiorwlock

import globalValues
import add

async def edit(ctx, args):

    if len(args) < 1:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, please input a card code.")
        return

    code = args[0]
    code = code.lower()

    card = await globalValues.catalog.getNextCatalogCard(code)
    if card == None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, that card could not be found.")
        return

    if card.getID() != ctx.author.id:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't own `" + code + "`.")
        return

    tickets = await globalValues.catalog.getUser(ctx.author.id).getTickets()
    coins = await globalValues.catalog.getUser(ctx.author.id).getCoins()

    preferredPaymentList = card.getPayment()
    preferredPaymentStr = card.getPaymentStr()

    currencyInfo = [card.getCurrencyType(), card.getCurrencyAmount()]

    currencyStr = "**" + str(currencyInfo[1]) + "** ยท "
    if currencyInfo[0] == '๐ซ':
        currencyStr += "๐ซ ยท `ticket"
    else:
        currencyStr += "๐ช ยท `coin"
    if currencyInfo[1] != 1:
        currencyStr += "s"
    currencyStr += "`"

    embedVar = discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n๐ : edit preferred payment\n๐ฐ : edit catalog payment")
    message = await ctx.channel.send(embed=embedVar)
    await message.add_reaction('๐')
    await message.add_reaction('๐ฐ')
    await message.add_reaction('โ')
    await message.add_reaction('โ')

    def editCheck(react, user):
        return react.message == message and user == ctx.author and (react.emoji == '๐' or react.emoji == '๐ฐ' or react.emoji == 'โ' or react.emoji == 'โ')

    while True:
        try:
            reaction = await globalValues.bot.wait_for('reaction_add', timeout=60, check=editCheck)
            reaction = reaction[0].emoji

            if reaction == '๐':
                preferredPaymentList = await add.getPreferredPayment(ctx)

            elif reaction == '๐ฐ':
                currencyInfo =  await add.getCurrency(ctx, tickets, coins)

            elif reaction == 'โ':
                success = await globalValues.catalog.editCard(code, preferredPaymentList, currencyInfo)
                if not success and currencyInfo[0] == '๐ซ':
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough tickets to add `" + code + "` to the catolog.")
                    raise asyncio.TimeoutError
                elif not success:
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough coins to add `" + code + "` to the catolog.")
                    raise asyncio.TimeoutError

                await message.edit(embed=discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n๐ต : edit preferred payment\n๐ฐ : edit catalog payment", color=discord.Color.green()))
                return
            else:
                raise asyncio.TimeoutError

            preferredPaymentStr = ""
            for emoji in preferredPaymentList:
                preferredPaymentStr += emoji + " ยท "
            preferredPaymentStr = preferredPaymentStr[:-3]

            currencyStr = "**" + str(currencyInfo[1]) + "** ยท "
            if currencyInfo[0] == '๐ซ':
                currencyStr += "๐ซ ยท `ticket"
            else:
                currencyStr += "๐ช ยท `coin"
            if currencyInfo[1] != 1:
                currencyStr += "s"
            currencyStr += "`"

            embedVar = discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n๐ : edit preferred payment\n๐ฐ : edit catalog payment")
            message = await ctx.channel.send(embed=embedVar)
            await message.add_reaction('๐')
            await message.add_reaction('๐ฐ')
            await message.add_reaction('โ')
            await message.add_reaction('โ')

        except asyncio.TimeoutError:
            await message.edit(embed=discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n๐ : edit preferred payment\n๐ฐ : edit catalog payment", color=discord.Color.red()))
            return