# catalog.py
# By: BentoBot02
# karuta catalog catalog command

import discord
import os
from discord.ext import commands
import aiorwlock
import time
import asyncio
from copy import deepcopy

import globalValues

async def catalog(ctx):

    catalogList = deepcopy(globalValues.catalog.getViewableCatalog().getPages())

    numPages = globalValues.catalog.getViewableCatalog().getNumPages()

    pageIndex = 0

    embedVar = discord.Embed(title="Karuta Catalog", description=catalogList[pageIndex].getPageStr(), color=0x6280D1)
    embedVar.set_image(url=catalogList[pageIndex].getImageURL())
    message = await ctx.channel.send(embed=embedVar)
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')

    def check(react, user):
        return react.message == message and user == ctx.author and (react.emoji == '⬅️' or react.emoji == '➡️')

    timeout = False
    while not timeout:

        try:
            reaction = await globalValues.bot.wait_for('reaction_add', timeout=60, check=check)
            reaction = reaction[0].emoji

            if reaction == '⬅️':
                if pageIndex > 0:
                    pageIndex -= 1

            else:
                if pageIndex < numPages - 1:
                    pageIndex += 1

            embedVar = discord.Embed(title="Karuta Catalog", description=catalogList[pageIndex].getPageStr(), color=0x6280D1)
            embedVar.set_image(url=catalogList[pageIndex].getImageURL())
            await message.edit(embed=embedVar)

        except asyncio.TimeoutError:
            timeout = True