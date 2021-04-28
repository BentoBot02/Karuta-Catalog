# invite.py
# By: BentoBot02
# karuta catalog invite command

import discord
import os
from discord.ext import commands

async def invite(ctx):

    dm = await ctx.author.create_dm()

    try:
        await dm.send("Invite Karuta Catalog into your server through this link:\n<https://discord.com/api/oauth2/authorize?client_id=PRIVATE&permissions=387136&scope=bot>")
    except:
        pass
    if str(ctx.channel.type) != 'private':
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, check your DM for the invite link.")

    