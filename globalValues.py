# globalValues.py
# By: BentoBot02
# contains the global values for KarutaCatalog

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import aiorwlock
import random
from operator import itemgetter
import urllib.request
from urllib.request import urlopen
from PIL import Image

from CatalogClass import Catalog

SERVER_ID = PRIVATE
RULES_CHANNEL_ID = PRIVATE
ANNOUNCEMENTS_CHANNEL_ID = PRIVATE
KARUTA_ID = 646937666251915264
HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

bot = None
catalog = None

CARD_COORDINATES = [(15, 20),
                    (315, 20),
                    (615, 20),
                    (915, 20),
                    (1215, 20),
                    (15, 490),
                    (315, 490),
                    (615, 490),
                    (915, 490),
                    (1215, 490)]

# noko club server id: 727898987285315736

def init(inbot, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, CLOUDFRONTURL, HEADER, NUM_PAGES, CARDS_PER_PAGE):
    global bot
    global catalog

    bot = inbot
    catalog = Catalog(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, CLOUDFRONTURL, HEADER, NUM_PAGES, CARDS_PER_PAGE)