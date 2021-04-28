# refresh.py
# By: BentoBot02
# karuta catalog refresh command

import discord
import os
from discord.ext import commands
import aiorwlock
import pickle

import globalValues

ANNOUNCEMENT_CHANNEL = PRIVATE

async def refresh(ctx):

    embedVars = await globalValues.catalog.refresh()
    pageStr = embedVars[0]
    image = embedVars[1]
    embedVar = discord.Embed(title="Karuta Catalog", description=pageStr, color=0x6280D1)
    embedVar.set_image(url=image)
    announcementChannel = globalValues.bot.get_channel(ANNOUNCEMENT_CHANNEL)
    message = await announcementChannel.send(embed=embedVar)
    await message.publish()

    await ctx.channel.send("<@" + str(ctx.author.id) + ">, inventories and catalogs have been refreshed.")