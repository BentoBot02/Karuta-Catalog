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

    currencyStr = "**" + str(currencyInfo[1]) + "** · "
    if currencyInfo[0] == '🎫':
        currencyStr += "🎫 · `ticket"
    else:
        currencyStr += "🪙 · `coin"
    if currencyInfo[1] != 1:
        currencyStr += "s"
    currencyStr += "`"

    embedVar = discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n💎 : edit preferred payment\n📰 : edit catalog payment")
    message = await ctx.channel.send(embed=embedVar)
    await message.add_reaction('💎')
    await message.add_reaction('📰')
    await message.add_reaction('❌')
    await message.add_reaction('✅')

    def editCheck(react, user):
        return react.message == message and user == ctx.author and (react.emoji == '💎' or react.emoji == '📰' or react.emoji == '❌' or react.emoji == '✅')

    while True:
        try:
            reaction = await globalValues.bot.wait_for('reaction_add', timeout=60, check=editCheck)
            reaction = reaction[0].emoji

            if reaction == '💎':
                preferredPaymentList = await add.getPreferredPayment(ctx)

            elif reaction == '📰':
                currencyInfo =  await add.getCurrency(ctx, tickets, coins)

            elif reaction == '✅':
                success = await globalValues.catalog.editCard(code, preferredPaymentList, currencyInfo)
                if not success and currencyInfo[0] == '🎫':
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough tickets to add `" + code + "` to the catolog.")
                    raise asyncio.TimeoutError
                elif not success:
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you don't have enough coins to add `" + code + "` to the catolog.")
                    raise asyncio.TimeoutError

                await message.edit(embed=discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n💵 : edit preferred payment\n📰 : edit catalog payment", color=discord.Color.green()))
                return
            else:
                raise asyncio.TimeoutError

            preferredPaymentStr = ""
            for emoji in preferredPaymentList:
                preferredPaymentStr += emoji + " · "
            preferredPaymentStr = preferredPaymentStr[:-3]

            currencyStr = "**" + str(currencyInfo[1]) + "** · "
            if currencyInfo[0] == '🎫':
                currencyStr += "🎫 · `ticket"
            else:
                currencyStr += "🪙 · `coin"
            if currencyInfo[1] != 1:
                currencyStr += "s"
            currencyStr += "`"

            embedVar = discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n💎 : edit preferred payment\n📰 : edit catalog payment")
            message = await ctx.channel.send(embed=embedVar)
            await message.add_reaction('💎')
            await message.add_reaction('📰')
            await message.add_reaction('❌')
            await message.add_reaction('✅')

        except asyncio.TimeoutError:
            await message.edit(embed=discord.Embed(title="Catalog Editor", description="Edit `" + code + "`\nPreferred payment:\n" + preferredPaymentStr + "\nCatalog Payment:\n" + currencyStr + "\n\n💎 : edit preferred payment\n📰 : edit catalog payment", color=discord.Color.red()))
            return