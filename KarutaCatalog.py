# KartuaCatalog.py
# By: BentoBot02
# karuta catalog code

import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiorwlock
import aioschedule as schedule
import asyncio

import api

from CatalogClass import Catalog

from verify import verify, checkVerification
from catalog import catalog
from lookup import lookup
from view import view
from add import add
from edit import edit
from remove import remove
from queue_command import queue
from live import live
from inventory import inventory
from vote import vote
from coins import coins
from cooldown import cooldown
from trade import trade
from exchange import exchange
from invite import invite
from givetickets import givetickets
from givecoins import givecoins
from save import save
from refresh import refresh

import globalValues

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.environ.get("PORT", 5000))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET = PRIVATE
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
NUM_PAGES = 10
CARDS_PER_PAGE = 10
SERVER_ID = PRIVATE
ANNOUNCEMENT_CHANNEL = PRIVATE

PREFIX = "kc!"

intents = discord.Intents(messages=True, reactions=True, invites=True, guilds=True, members=True, emojis=True)
bot = commands.Bot(command_prefix=['kc!', 'KC!', 'Kc!', 'kC!'], case_insensitive=True, help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    globalValues.init(bot, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, CLOUDFRONT_URL, HEADER, NUM_PAGES, CARDS_PER_PAGE)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="catalog in " + str(len(bot.guilds)) + " servers"))
    refresh_catalog_loop.start()

firstPass = True
@tasks.loop(hours=13)
async def refresh_catalog_loop():
    global firstPass
    if not firstPass:
        embedVars = await globalValues.catalog.refresh()
        pageStr = embedVars[0]
        image = embedVars[1]
        embedVar = discord.Embed(title="Karuta Catalog", description=pageStr, color=0x6280D1)
        embedVar.set_image(url=image)
        announcementChannel = bot.get_channel(ANNOUNCEMENT_CHANNEL)
        message = await announcementChannel.send(embed=embedVar)
        await message.publish()
    firstPass = False


@bot.command(
    name="add",
    aliases=["a"])
async def add_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await add(ctx, args)


@bot.command(
    name="edit",
    aliases=["e"])
async def edit_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await edit(ctx, args)
    

@bot.command(
    name="remove",
    aliases=["r"])
async def remove_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await remove(ctx, args)


@bot.command(
    name="queue",
    aliases=["q"])
async def queue_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await queue(ctx, args)


@bot.command(
    name="live",
    aliases=["l"])
async def live_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await live(ctx, args)


@bot.command(
    name = "catalog",
    aliases=["c"])
async def catalog_command(ctx):
    await catalog(ctx)


@bot.command(
    name="view",
    aliases=["v"])
async def view_command(ctx, *args):
    await view(ctx, args)


@bot.command(
    name="lookup",
    aliases=["lu"])
async def lookup_command(ctx, *args):
    await lookup(ctx, args)


@bot.command(
    name="inventory",
    aliases=["inv", "i"])
async def inventory_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await inventory(ctx, args)


@bot.command(name="vote")
async def vote_command(ctx):
    verified = await checkVerification(ctx)
    if verified:
        await vote(ctx)


@bot.command(name="coins")
async def coins_command(ctx):
    verified = await checkVerification(ctx)
    if verified:
        await coins(ctx)
    

@bot.command(
    name="cooldown",
    aliases=["cd"])
async def cooldown_command(ctx, *args):
    verified = await checkVerification(ctx)
    if verified:
        await cooldown(ctx, args)


@bot.command(
    name="trade",
    aliases=["t"])
async def trade_command(ctx, id):
    verified = await checkVerification(ctx)
    if verified:
        await trade(ctx, id)


@bot.command(
    name="exchange",
    aliases=["x"])
async def exchange_command(ctx):
    verified = await checkVerification(ctx)
    if verified:
        await exchange(ctx)


@bot.command(name="verify")
async def verify_command(ctx):
    await verify(ctx)


@bot.command(name="invite")
async def invite_command(ctx):
    await invite(ctx)


@bot.group(name="help", invoke_without_command=True)
async def help_command(ctx):
    embedVar = discord.Embed(title="Karuta Catalog Commands", description="The full list of commands.", color=0x6280D1)
    embedVar.add_field(name="Catalog Queue Commands", value="`add`, `edit`, `remove`, `queue`, `live`", inline=False)
    embedVar.add_field(name="Live Catalog Commands", value="`catalog`, `view`, `lookup`", inline=False)
    embedVar.add_field(name="Economy Commands", value="`inventory`, `vote`, `coins`, `cooldown`, `trade`", inline=False)
    embedVar.add_field(name="Administrative Commands", value="`verify`, `invite`", inline=False)
    embedVar.set_footer(text="Type kc!help <command> for more info on a command.")
    dm = await ctx.author.create_dm()
    try:
        await dm.send(embed=embedVar)
    except:
        pass
    if str(ctx.channel.type) != 'private':
        await ctx.channel.send("<@" + str(ctx.author.id) + ">, check your DM for the list of commands.")

@help_command.command(
    name="add",
    aliases=["a"])
async def help_add_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!add`", description="Alias: `a`\nFormat: `kc!add <card code>`\n\nAdds a card to the catalog queue.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="edit",
    aliases=["e"])
async def help_ediit_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!edit`", description="Alias: `e`\nFormat: `kc!edit <card code>`\n\nEdits a card's preferred payment and catalog payment.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="remove",
    aliases=["r"])
async def help_remove_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!remove`", description="Alias: `r`\nFormat: `kc!remove <card code>`\n\nRemoves a card from the catalog queue.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name = "queue",
    aliases=["q"])
async def help_catalog_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!queue`", description="Alias: `q`\nFormat: `kc!queue` *`<user>`*\n\nView your or another user's cards that are currently waiting in the queue.", color=0x6280D1)
    embedVar.set_footer(text="Optional values are in italics.")
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name = "live",
    aliases=["l"])
async def help_catalog_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!live`", description="Alias: `l`\nFormat: `kc!live` *`<user>`*\n\nView your or another user's cards that are currently in the live catalog.", color=0x6280D1)
    embedVar.set_footer(text="Optional values are in italics.")
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name = "catalog",
    aliases=["c"])
async def help_catalog_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!catalog`", description="Alias: `c`\n\nView the viewable catalog.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="view",
    aliases=["v"])
async def help_view_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!view`", description="Alias: `v`\nFormat: `kc!view <card code>`\n\nView a card in the live catalog.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="lookup",
    aliases=["lu"])
async def help_lookup_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!lookup`", description="Alias: `lu`\nFormat: `kc!lookup` *`<parameters>`*\nExample:`kc!lookup s:demon slayer c:tanjiro q=4 p<100 e=2`\n\n"
            "Look up cards in the live catalog.\n"
            "```ml\n"
            "Parameters:\n"
            "quality | q\n"
            "print | p\n"
            "edition | e\n"
            "series | s\n"
            "character | c\n"
            "\n"
            "Operators:\n"
            ":  - all parameters\n"
            "=  - all parameters\n"
            "<= - quality, print, edition\n"
            "<  - quality, print, edition\n"
            ">= - quality, print, edition\n"
            ">  - quality, print, edition\n"
            "```",
            color=0x6280D1)
    await ctx.channel.send(embed=embedVar)
    
@help_command.command(
    name="inventory",
    aliases=["inv", "i"])
async def help_inventory_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!inventory`", description="Aliases: `inv`, `i`\nFormat: `kc!inventory` *`<user>`*\n\n\nView the inventory of yourself or another user.", color=0x6280D1)
    embedVar.set_footer(text="Optional values are in italics.")
    await ctx.channel.send(embed=embedVar)

@help_command.command(name="vote")
async def help_vote_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!vote`", description="Vote for Karuta Catalog to recieve 2 tickets on weekdays and 4 on the weekend.\nVote for PRIVATE to recieve 1 ticket.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(name="coins")
async def help_coins_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!coins`", description="Purchase coins through DonateBot. Type the number of the desired product, and click the link to go to the store.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="cooldown",
    aliases=["cd"])
async def help_cooldown_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!cooldown`", description="Alias: `cd`\nFormat: `kc!cooldown` *`<user>`*\n\nView your or another user's voting cooldown times.", color=0x6280D1)
    embedVar.set_footer(text="Optional values are in italics.")
    await ctx.channel.send(embed=embedVar)

@help_command.command(name="trade")
async def help_trade_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!trade`", description="Alias: `t`\nFormat: `kc!trade` `<user>`\n\nInitiate a trade with another user.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(
    name="exchange",
    aliases=["x"])
async def help_cooldown_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!exchange`", description="Alias: `x`\n\nExchange coins for tickets.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(name="verify")
async def help_coins_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!verify`", description="Verifies the user. A user must be verified to use the majorty of the commands.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)

@help_command.command(name="invite")
async def help_invite_subcommand(ctx):
    embedVar = discord.Embed(title="Command Info: `kc!invite`", description="DM a link to add Karuta Catalog to your own server.", color=0x6280D1)
    await ctx.channel.send(embed=embedVar)


@bot.event
async def on_guild_join(guild):

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hey there! Thank you for inviting Karuta Catalog to your server.\nJoin this server to add cards to the catalog and stay in the loop on updates and bug fixes. You must join this server to add cards to the catalog. This will ensure buyers can DM you and not just see a Discord ID.\nhttps://discord.gg/dKcRrJP9dT")
            break
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="catalog in " + str(len(bot.guilds)) + " servers"))

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="catalog in " + str(len(bot.guilds)) + " servers"))

@bot.command(
    name="givecoins",
    aliases=["gc"])
@commands.is_owner()
async def givecoins_command(ctx, id, amount):
    await givecoins(ctx, id, amount)

@bot.command(
    name="givetickets",
    aliases=["gt"])
@commands.is_owner()
async def givetickets_command(ctx, id, amount):
    await givetickets(ctx, id, amount)

@bot.command(name="save")
@commands.is_owner()
async def save_command(ctx):
    await save(ctx)

@bot.command(name="refresh")
@commands.is_owner()
async def refresh_command(ctx):
    refresh_catalog_loop.restart()
    await ctx.channel.send("<@" + str(ctx.author.id) + ">, inventories and catalogs have been refreshed.")

bot.loop.create_task(api.app.run_task(host='0.0.0.0', port=PORT))

bot.run(TOKEN)