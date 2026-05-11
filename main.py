import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
import yfinance as yf
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

BOT_TZ = ZoneInfo(os.getenv("BOT_TZ", "Asia/Tehran"))

def get_prices():
    prices = {}

    # btc, eth
    crypto_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd").json()
    prices["btc"] = crypto_data["bitcoin"]["usd"]
    prices["eth"] = crypto_data["ethereum"]["usd"]

    # gold, silver, oil
    symbols = ["GC=F", "SI=F", "CL=F"]
    assets = yf.Tickers(symbols)
    prices["gold"] = assets.tickers["GC=F"].fast_info['last_price']
    prices["silver"] = assets.tickers["SI=F"].fast_info['last_price']
    prices["oil"] = assets.tickers["CL=F"].fast_info['last_price']

    # usdt
    nobitex_data = requests.get(
        "https://apiv2.nobitex.ir/market/stats?srcCurrency=usdt&dstCurrency=rls"
    ).json()
    prices["usdt"] = int(nobitex_data["stats"]["usdt-rls"]["latest"])

    return prices

async def main():
    bot = Bot(token=BOT_TOKEN)

    while True:
        now = datetime.now(BOT_TZ)
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        wait_seconds = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        await bot.send_message(chat_id=CHANNEL_ID, text=get_prices())

if __name__ == "__main__":
    asyncio.run(main())
