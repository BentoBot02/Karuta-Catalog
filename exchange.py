# exchange.py
# By: PVCPipe01
# karuta catalog exchange command

import discord
import os
from discord.ext import commands, tasks
import asyncio

async def exchange(ctx):

    embedVar = discord.Embed(title="Catalog Exchange", description="Exchange coins for tickets.\n\nLet me know what the exchange rate should be.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)