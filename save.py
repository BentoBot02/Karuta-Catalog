# add.py
# By: BentoBot02
# karuta catalog add command

import discord
import os
from discord.ext import commands
import aiorwlock
import pickle

import globalValues

async def save(ctx):

    await globalValues.catalog.save()

    await ctx.channel.send("<@" + str(ctx.author.id) + ">, inventories and catalogs have been saved.")