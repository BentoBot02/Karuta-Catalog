# inventory.py
# By: BentoBot02
# karuta catalog inventory command

import discord
import os
from discord.ext import commands
import aiorwlock

import globalValues

async def inventory(ctx, args):

    if len(args) != 0:
        id = None
        try:
            id = int(args[0].replace('<', '').replace('!', '').replace('@', '').replace('>', ''))
        except ValueError:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user was not found.")
            return

        if globalValues.catalog.getUser(id) == None:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user was not found.")
            return

        numTickets = await globalValues.catalog.getUser(id).getTickets()
        numCoins = await globalValues.catalog.getUser(id).getCoins()

        descriptionStr = "Items carried by <@" + str(id) + ">\n\n🎫 **" + str(numTickets) + "** · `ticket` · *Ticket*\n🪙 **" + str(numCoins) + "** · `coin` · *Coin*"
        embedVar = discord.Embed(title="Inventory", description=descriptionStr, color=0x6280D1)
        await ctx.channel.send(embed=embedVar)

    else:
        numTickets = await globalValues.catalog.getUser(ctx.author.id).getTickets()
        numCoins = await globalValues.catalog.getUser(ctx.author.id).getCoins()

        descriptionStr = "Items carried by <@" + str(ctx.author.id) + ">\n\n🎫 **" + str(numTickets) + "** · `ticket` · *Ticket*\n🪙 **" + str(numCoins) + "** · `coin` · *Coin*"
        embedVar = discord.Embed(title="Inventory", description=descriptionStr, color=0x6280D1)
        await ctx.channel.send(embed=embedVar)