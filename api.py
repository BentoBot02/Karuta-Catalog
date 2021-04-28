# api.py
# By: BentoBot02
# hold the Flask app for donations and votes

import os
from quart import Quart, request
from threading import Thread
from dotenv import load_dotenv

import gspread

import globalValues

load_dotenv()
DONATION_AUTH_CODE = os.getenv("DONATION_AUTH_CODE")
VOTE_AUTH_CODE = os.getenv("VOTE_AUTH_CODE")
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")
COINS_1 = os.getenv("COINS_1")
COINS_2 = os.getenv("COINS_2")
COINS_5 = os.getenv("COINS_5")
COINS_10 = os.getenv("COINS_10")
COINS_20 = os.getenv("COINS_20")
COINS_50 = os.getenv("COINS_50")
COINS_100 = os.getenv("COINS_100")
COINS_200 = os.getenv("COINS_200")

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key(SPREADSHEET_KEY)

app = Quart('')
  
@app.route("/donation/", methods=['POST'])
async def quart_donation():
    
    if request.headers.get('Authorization') == DONATION_AUTH_CODE:

        worksheet = sh.sheet1

        dictionary = await request.get_json()

        try:
            buyer_email = dictionary.get('buyer_email')
            raw_buyer_id = dictionary.get('raw_buyer_id')
            raw_buyer_id = int(raw_buyer_id)
            guild_id = dictionary.get('guild_id')
            price = dictionary.get('price')
            currency = dictionary.get('currency')
            recurring = dictionary.get('recurring')
            status = dictionary.get('status')
            role_id = dictionary.get('role_id')
            product_id = dictionary.get('product_id')
            seller_email = dictionary.get('seller_email')
            txn_id = dictionary.get('txn_id')
            valid_price = dictionary.get('valid_price')

            if str(product_id) == str(COINS_1):
                await globalValues.catalog.addCoins(raw_buyer_id, 100)

            elif str(product_id) == str(COINS_2):
                await globalValues.catalog.addCoins(raw_buyer_id, 220)

            elif str(product_id) == str(COINS_5):
                await globalValues.catalog.addCoins(raw_buyer_id, 600)

            elif str(product_id) == str(COINS_10):
                await globalValues.catalog.addCoins(raw_buyer_id, 1300)

            elif str(product_id) == str(COINS_20):
                await globalValues.catalog.addCoins(raw_buyer_id, 2800)

            elif str(product_id) == str(COINS_50):
                await globalValues.catalog.addCoins(raw_buyer_id, 7500)

            elif str(product_id) == str(COINS_100):
                await globalValues.catalog.addCoins(raw_buyer_id, 16000)

            elif str(product_id) == str(COINS_200):
                await globalValues.catalog.addCoins(raw_buyer_id, 34000)

            raw_buyer_id = str(raw_buyer_id)
            guild_id = str(guild_id)
            row = [buyer_email, raw_buyer_id, guild_id, price, currency, recurring, status, role_id, product_id, seller_email, txn_id, valid_price]
            worksheet.append_row(row)
        except (TypeError, ValueError):
            pass

    return "Donation Recieved", 200

@app.route("/vote/bot/", methods=['POST'])   
async def quart_bot_vote():

    if request.headers.get('Authorization') == VOTE_AUTH_CODE:

        worksheet = sh.get_worksheet(1)

        dictionary = await request.get_json()

        try:
            numVotes = 2
            bot_id = dictionary.get('bot')
            try:
                bot_id = int(bot_id)
            except (TypeError, ValueError) as e:
                pass
            user = dictionary.get('user')
            try:
                user = int(user)
            except (TypeError, ValueError) as e:
                pass
            type = dictionary.get('type')
            isWeekend = dictionary.get('isWeekend')

            if bot_id == PRIVATE:
                if isWeekend == True:
                    numVotes = 4

                await globalValues.catalog.addTickets(user, numVotes)
                globalValues.catalog.setBotVote(user)

                user = str(user)
                bot_id = str(bot_id)

                row = [user, bot_id, type, isWeekend, numVotes]
                worksheet.append_row(row)
        except ValueError:
            pass

@app.route("/vote/server/", methods=['POST'])   
async def quart_server_vote():

    if request.headers.get('Authorization') == VOTE_AUTH_CODE:

        worksheet = sh.get_worksheet(2)

        dictionary = await request.get_json()

        try:
            numVotes = 1
            guild_id = dictionary.get('guild')
            try:
                guild_id = int(guild_id)
            except (TypeError, ValueError) as e:
                pass
            user = dictionary.get('user')
            try:
                user = int(user)
            except (TypeError, ValueError) as e:
                pass
            type = dictionary.get('type')
            isWeekend = dictionary.get('isWeekend')

            if guild_id == PRIVATE:

                await globalValues.catalog.addTickets(user, numVotes)
                globalValues.catalog.setServerVote(user)

                user = str(user)
                guild_id = str(guild_id)

                row = [user, guild_id, type, numVotes]
                worksheet.append_row(row)
        except ValueError:
            pass

    return "Vote Recieved", 200