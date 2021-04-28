# coins.py
# By: BentoBot02
# karuta catalog coins command

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

import globalValues

load_dotenv()
COINS_1 = os.getenv("COINS_1")
COINS_2 = os.getenv("COINS_2")
COINS_5 = os.getenv("COINS_5")
COINS_10 = os.getenv("COINS_10")
COINS_20 = os.getenv("COINS_20")
COINS_50 = os.getenv("COINS_50")
COINS_100 = os.getenv("COINS_100")
COINS_200 = os.getenv("COINS_200")

async def coins(ctx):

    priceStr = str("Type the number of the desired item." +
               "```md\n" +
               "1. <$1.00> 100 Coins\n" +
               "2. <$2.00> 220 Coins (200 + 20 bonus)\n" +
               "3. <$5.00> 600 Coins (500 + 100 bonus)\n" +
               "4. <$10.00> 1,300 Coins (1,000 + 300 bonus)\n" +
               "5. <$20.00> 2,800 Coins (2,000 + 800 bonus)\n" +
               "6. <$50.00> 7,500 Coins (5,000 + 2,500 bonus)\n" +
               "7. <$100.00> 16,000 Coins (10,000 + 6,000 bonus)\n" +
               "8. <$200.00> 34,000 Coins (20,000 + 14,000 bonus)```")

    embedVar = discord.Embed(title="Purchase Coins", description=priceStr, color=0x6280D1)
    embedVar.set_footer(text="Thank you for supporting Karuta Catalog!\nDM BentoBot#8263 if you have any issues.")
    coinMessage = await ctx.channel.send(embed=embedVar)

    def coinsCheck(m):
        return m.channel == ctx.channel and m.author == ctx.author

    try:
        message = await globalValues.bot.wait_for('message', timeout=30, check=coinsCheck)

        num = int(message.content.split()[0])
        linkStr = "<@" + str(ctx.author.id) + ">, please follow this link to complete your purchase: <https://donatebot.io/checkout/727898987285315736"
        if num == 1:
            linkStr += "?id=" + COINS_1 + "&buyer=" + str(ctx.author.id)
        elif num == 2:
            linkStr += "?id=" + COINS_2 + "&buyer=" + str(ctx.author.id)
        elif num == 3:
            linkStr += "?id=" + COINS_5 + "&buyer=" + str(ctx.author.id)
        elif num == 4:
            linkStr += "?id=" + COINS_10 + "&buyer=" + str(ctx.author.id)
        elif num == 5:
            linkStr += "?id=" + COINS_20 + "&buyer=" + str(ctx.author.id)
        elif num == 6:
            linkStr += "?id=" + COINS_50 + "&buyer=" + str(ctx.author.id)
        elif num == 7:
            linkStr += "?id=" + COINS_100 + "&buyer=" + str(ctx.author.id)
        elif num == 8:
            linkStr += "?id=" + COINS_200 + "&buyer=" + str(ctx.author.id)
        elif num > 8:
            return

        await ctx.channel.send(linkStr + ">")


    except (asyncio.TimeoutError, ValueError) as e:
        embedVar = discord.Embed(title="Purchase Coins", description=priceStr, color=discord.Color.red())
        embedVar.set_footer(text="Thank you for supporting Karuta Catalog!\nDM BentoBot#8263 if you have any issues.")
        await coinMessage.edit(embed=embedVar)

    