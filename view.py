# view.py
# By: BentoBot02
# karuta catalog view command

import discord
import os
from discord.ext import commands
from copy import deepcopy

import globalValues

async def view(ctx, args):

    if len(args) < 1:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, please input a card code.")
        return

    code = args[0]
    code = code.lower()

   
    card = await globalValues.catalog.getLiveCatalogCard(code)

    if card == None:
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, that card is not in the catalog.")
        return

    descriptionStr = card.getViewStr()
    preferredPaymentStr = card.getPaymentStr()

    embedVar = discord.Embed(title="Card Details", description=descriptionStr, color=0x6280D1)
    embedVar.add_field(name="Preferred Payment:", value=preferredPaymentStr)
    embedVar.set_image(url=card.getImageURL())
    await ctx.channel.send(embed=embedVar)