import requests
import yfinance as yf

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

    return prices

def main():
    print(get_prices())

if __name__ == "__main__":
    main()
