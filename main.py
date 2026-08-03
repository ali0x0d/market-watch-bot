import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Bot

from market_data import get_crypto_prices, get_commodity_prices, get_usdt_price

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

BOT_TZ = ZoneInfo(os.getenv("BOT_TZ", "Asia/Tehran"))

def format_price_message(prices):
    now = datetime.now(BOT_TZ).strftime("%Y-%m-%d %H:%M")

    return (
        f"🕒 {now}\n\n"
        f" ₿  BTC:     ${prices['btc']:,.0f}\n"
        f" ⟠  ETH:     ${prices['eth']:,.0f}\n\n"
        f"🥇 Gold:    ${prices['gold']:,.0f}\n"
        f"🥈 Silver:  ${prices['silver']:,.2f}\n"
        f"🛢 Oil:       ${prices['oil']:,.2f}\n\n"
        f"💵 USDT:  {prices['usdt']/10:,.0f} IRT"
    )

async def get_prices():
    crypto_prices, commodity_prices, usdt_price = await asyncio.gather(
        asyncio.to_thread(get_crypto_prices),
        asyncio.to_thread(get_commodity_prices),
        asyncio.to_thread(get_usdt_price),
    )

    return {**crypto_prices, **commodity_prices, **usdt_price}

async def main():
    bot = Bot(token=BOT_TOKEN)

    while True:
        now = datetime.now(BOT_TZ)
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        wait_seconds = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        prices = await get_prices()
        msg = format_price_message(prices)
        await bot.send_message(chat_id=CHANNEL_ID, text=msg)

if __name__ == "__main__":
    asyncio.run(main())
