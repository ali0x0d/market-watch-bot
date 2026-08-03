import requests
import yfinance as yf

def get_crypto_prices():
    # btc, eth
    crypto_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=10).json()

    return {
        "btc": crypto_data["bitcoin"]["usd"],
        "eth": crypto_data["ethereum"]["usd"],
    }

def get_commodity_prices():
    # gold, silver, oil
    symbols = ["GC=F", "SI=F", "CL=F"]
    assets = yf.Tickers(symbols)

    return {
        "gold": assets.tickers["GC=F"].fast_info['last_price'],
        "silver": assets.tickers["SI=F"].fast_info['last_price'],
        "oil": assets.tickers["CL=F"].fast_info['last_price'],
    }

def get_usdt_price():
    # usdt
    nobitex_data = requests.get(
        "https://apiv2.nobitex.ir/market/stats?srcCurrency=usdt&dstCurrency=rls",
        timeout=10
    ).json()

    return {
        "usdt": int(nobitex_data["stats"]["usdt-rls"]["latest"])
    }