# verify.py
# By: BentoBot02
# karuta catalog verify command

import discord
import os
from discord.ext import commands, tasks
import aiorwlock

from CatalogUserClass import CatalogUser
import globalValues

async def verify(ctx):

    if globalValues.catalog.getUser(ctx.author.id) == None:
        globalValues.catalog.verify(ctx.author.id)

        await ctx.channel.send("<@" + str(ctx.author.id) + ">, you are now verified! Enjoy 2 free Karuta Catalog tickets!")

##############################################################################################################################################

async def checkVerification(ctx):

    if globalValues.catalog.getUser(ctx.author.id) == None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, you must be verified to use this command. Type `kc!verify` to get started!")
        return False
    else:
        return True