# cooldown.py
# By: BentoBot02
# holds the cooldown command

import discord
import os
from discord.ext import commands, tasks
import asyncio

import globalValues

async def cooldown(ctx, args):
    
    id = None
    if len(args) > 0:
        id = args[0].replace('<', '').replace('@', '').replace('!', '').replace('>', '')
        try:
            id = int(id)
            if globalValues.catalog.getUser(id) == None:
                raise ValueError
        except ValueError:
            await ctx.channel.send("<@" + str(ctx.author.id) + ">, that user was not found.")
            return
    else:
        id = ctx.author.id

    serverVote = globalValues.catalog.getServerVoteStr(id)
    botVote = globalValues.catalog.getBotVoteStr(id)

    descriptionStr = "Showing cooldowns for <@" + str(id) + ">\n\n"
    descriptionStr += botVote + "\n"
    descriptionStr += serverVote + "\n"

    embedVar = discord.Embed(title="Catalog Cooldowns", description=descriptionStr, color=0x6280D1)
    await ctx.channel.send(embed=embedVar)