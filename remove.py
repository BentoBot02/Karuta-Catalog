# remove.py
# By: BentoBot02
# karuta catalog remove command

import discord
import os
from discord.ext import commands

import globalValues

async def remove(ctx, args):
    
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

    await globalValues.catalog.popCard(code)
    await ctx.channel.send("<@" + str(ctx.author.id) + ">, `" + code + "` was successfully removed.")