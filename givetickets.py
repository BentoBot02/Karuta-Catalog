# givetickets.py
# By: BentoBot02
# holds the givetickets command

import discord
import os
from discord.ext import commands, tasks
import aiorwlock

import globalValues

async def givetickets(ctx, id, amount):

    try:
        id = int(id.replace('<', '').replace('!', '').replace('@', '').replace('>', ''))
        amount = int(amount)
    except ValueError:
        return

    if globalValues.catalog.getUser(id) == None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user could not be found.")
        return

    await globalValues.catalog.addTickets(id, amount)

    await ctx.channel.send("<@" + str(ctx.author.id) + ">, <@" + str(id) + "> has recieved " + str(amount) + " tickets.")