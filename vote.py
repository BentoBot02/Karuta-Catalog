# vote.py
# By: BentoBot02
# karuta catalog vote command

import discord
import os
from discord.ext import commands
import aiorwlock

import globalValues

async def vote(ctx):

    await ctx.channel.send("<https://top.gg/servers/PRIVATE/vote>" + "\nVote for PRIVATE.")