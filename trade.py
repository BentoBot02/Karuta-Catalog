# trade.py
# By: BentoBot02
# karuta catalog trade command

import discord
import os
from discord.ext import commands
import asyncio

import globalValues

async def trade(ctx, id):

    try:
        id = int(id.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
        user = globalValues.catalog.getUser(id)
        member = ctx.guild.get_member(id)
        if user == None or member == None:
            raise ValueError

    except ValueError:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user could not be found.")
        return

    if ctx.author.id == id:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, you cannot trade with yourself.")
        return

    embedVar = discord.Embed(title="Catalog Trade Request", description="<@" + str(id) + ">, please accept or decline the trade request with <@" + str(ctx.author.id) + "> to continue.", color=0x6280D1)
    message = await ctx.channel.send(content="<@" + str(id) + ">, would you to trade with <@" + str(ctx.author.id) + ">?", embed=embedVar)

    await message.add_reaction('❌')
    await message.add_reaction('☑️')

    def tradeCheck(react, user):
        return react.message == message and ((user.id == id or user == ctx.author) and react.emoji == '❌') or ((user.id == id and react.emoji == '☑️'))

    try:
        reaction = await globalValues.bot.wait_for('reaction_add', timeout=60, check=tradeCheck)
        reaction = reaction[0].emoji

        if reaction == '☑️':
            class TradeInfo:
                class Trader:
                    def __init__(self, id, origTickets, origCoins):
                        self.id = id
                        self.tickets = 0
                        self.coins = 0
                        self.origTickets = origTickets
                        self.origCoins = origCoins
                        self.string = ""
                        self.ready = False
                        self.setString()

                    def setString(self):
                        tempStr = ""
                        if self.ready:
                            tempStr += "```diff\n+ Ready +\n\n"
                        else:
                            tempStr += "```diff\n- Not Ready -\n\n"
                        if self.tickets > 0:
                            tempStr += str(self.tickets) + " tickets\n"
                        if self.coins > 0:
                            tempStr += str(self.coins) + " coins\n"
                        tempStr = tempStr.strip()
                        tempStr += "```"
                        self.string = tempStr

                def __init__(self, id0, id1, message, embedVar, origTickets0=0, origCoins0=0, origTickets1=0, origCoins1=0):
                    self.trader0 = self.Trader(id0, origTickets0, origCoins0)
                    self.trader1 = self.Trader(id1, origTickets1, origCoins1)
                    self.message = message
                    self.embedVar = embedVar

                async def tradeListener(self, m):
                    if m.channel == ctx.channel and (m.author.id == self.trader0.id and not self.trader0.ready or m.author.id == self.trader1.id and not self.trader1.ready):
                        try:
                            mList = m.content.split()
                            num = int(mList[0])
                            item = mList[1]

                            if m.author.id == self.trader0.id:
                                if "ticket" in item or item == '🎫':
                                    if self.trader0.origTickets < num:
                                        await ctx.channel.send("<@" + str(self.trader0.id) + ">, you don't have `" + str(num) + "` tickets.")
                                        return
                                    self.trader0.tickets = num
                                elif "coin" in item or item == '🪙':
                                    if self.trader0.origCoins < num:
                                        await ctx.channel.send("<@" + str(self.trader0.id) + ">, you don't have `" + str(num) + "` coins.")
                                        return
                                    self.trader0.coins = num
                            else:
                                if "ticket" in item or item == '🎫':
                                    if self.trader1.origTickets < num:
                                        await ctx.channel.send("<@" + str(self.trader1.id) + ">, you don't have `" + str(num) + "` tickets.")
                                        return
                                    self.trader1.tickets = num
                                elif "coin" in item or item == '🪙':
                                    if self.trader1.origCoins < num:
                                        await ctx.channel.send("<@" + str(self.trader1.id) + ">, you don't have `" + str(num) + "` coins.")
                                        return
                                    self.trader1.coins = num
                            
                            self.trader0.setString()
                            self.trader1.setString()
                            self.embedVar.set_field_at(0, name=globalValues.bot.get_user(self.trader0.id).name, value=self.trader0.string)
                            self.embedVar.set_field_at(1, name=globalValues.bot.get_user(self.trader1.id).name, value=self.trader1.string)
                            await self.message.edit(embed=self.embedVar)
                        except (IndexError, ValueError):
                            return
                    

                async def readyListener(self, react, user):
                    if user.id == self.trader0.id and react.emoji == '🔒':
                        self.trader0.ready = True
                        self.trader0.setString()
                        embedVar.set_field_at(0, name=globalValues.bot.get_user(self.trader0.id).name, value=self.trader0.string)
                        await message.edit(embed=embedVar)
                    elif user.id == id and react.emoji == '🔒':
                        self.trader1.ready = True
                        self.trader1.setString()
                        embedVar.set_field_at(1, name=globalValues.bot.get_user(self.trader1.id).name, value=self.trader1.string)
                        await message.edit(embed=self.embedVar)

                def lockCheck(self, react, user):
                    if (user.id == self.trader0.id or user.id == self.trader1.id) and react.emoji == '❌':
                        return True
                    if user.id == self.trader0.id and react.emoji == '🔒':
                        self.trader0.ready = True
                    elif user.id == self.trader1.id and react.emoji == '🔒':
                        self.trader1.ready = True
                    if self.trader0.ready and self.trader1.ready:
                        return True
                    return False

            embedVar = discord.Embed(title="Trade", description="Type `<#>` `<item>` to add to the trade.", color=0x6280D1)
            embedVar.add_field(name=globalValues.bot.get_user(ctx.author.id).name, value="```diff\n- Not Ready -```")
            embedVar.add_field(name=globalValues.bot.get_user(id).name, value="```diff\n- Not Ready -```")
            embedVar.set_footer(text="You have 10 minutes to input your items. You both must lock your items before proceeding to the next step.")
            await message.edit(embed=embedVar)
            await message.add_reaction('🔒')

            trader0Tickets = await globalValues.catalog.getUser(ctx.author.id).getTickets()
            trader0Coins = await globalValues.catalog.getUser(ctx.author.id).getCoins()
            trader1Tickets = await globalValues.catalog.getUser(id).getTickets()
            trader1Coins = await globalValues.catalog.getUser(id).getCoins()
            currentTrade = TradeInfo(ctx.author.id, id, message, embedVar, trader0Tickets, trader0Coins, trader1Tickets, trader1Coins)

            try:
                globalValues.bot.add_listener(currentTrade.tradeListener, 'on_message')
                globalValues.bot.add_listener(currentTrade.readyListener, 'on_reaction_add')
                reaction = await globalValues.bot.wait_for('reaction_add', timeout=600, check=currentTrade.lockCheck)
                globalValues.bot.remove_listener(currentTrade.tradeListener, name='on_message')
                globalValues.bot.remove_listener(currentTrade.readyListener, name='on_reaction_add')
                reaction = reaction[0].emoji
                if reaction == '❌':
                    embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has been declined.", color=discord.Color.red())
                    await message.edit(embed=embedVar)
                    return

                embedVar = discord.Embed(title="Trade", description="This trade has been locked.\nCarefully review the details and either accept or decline the offer.", color=0x6280D1)
                embedVar.add_field(name=globalValues.bot.get_user(currentTrade.trader0.id).name, value=currentTrade.trader0.string)
                embedVar.add_field(name=globalValues.bot.get_user(currentTrade.trader1.id).name, value=currentTrade.trader1.string)
                await message.edit(embed=embedVar)
                await message.add_reaction('✅')

                reactions = [False, False]

                def confirmCheck(react, user):
                    if (user == ctx.author or user.id == id) and react.emoji == '❌':
                        return True
                    if user == ctx.author and react.emoji == '✅':
                        reactions[0] = True
                    elif user.id == id and react.emoji == '✅':
                        reactions[1] = True
                    if reactions[0] and reactions[1]:
                        return True
                    return False

                try:
                    reaction = await globalValues.bot.wait_for('reaction_add', timeout=30, check=confirmCheck)
                    reaction = reaction[0].emoji
                    if reaction == '❌':
                        embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has been declined.", color=discord.Color.red())
                        await message.edit(embed=embedVar)
                        return
                    trades = [[currentTrade.trader0.tickets, currentTrade.trader0.coins], [currentTrade.trader1.tickets, currentTrade.trader1.coins]]
                    success = await globalValues.catalog.trade(ctx.author.id, trades[0], id, trades[1])
                    if not success:
                        raise asyncio.TimeoutError

                    embedVar = discord.Embed(title="Trade", description="**The trade has been accepted.**")
                    embedVar.add_field(name=globalValues.bot.get_user(currentTrade.trader0.id).name, value=currentTrade.trader0.string)
                    embedVar.add_field(name=globalValues.bot.get_user(currentTrade.trader1.id).name, value=currentTrade.trader1.string)
                    await message.edit(embed=embedVar)
                    return

                except asyncio.TimeoutError:
                    embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has expired.", color=discord.Color.red())
                    await message.edit(embed=embedVar)
                    return

            except asyncio.TimeoutError:
                globalValues.bot.remove_listener(tradeListener, name='on_message')
                globalValues.bot.remove_listener(readyListener, name='on_reaction_add')
                embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has expired.", color=discord.Color.red())
                await message.edit(embed=embedVar)
                return

        else:
            embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has been declined.", color=discord.Color.red())
            await message.edit(embed=embedVar)
            return

    except asyncio.TimeoutError:
        embedVar = discord.Embed(title="Catalog Trade Request", description="This trade has expired.", color=discord.Color.red())
        await message.edit(embed=embedVar)