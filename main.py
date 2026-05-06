import requests

def get_prices():
    prices = {}

    crypto_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd").json()
    prices["btc"] = crypto_data["bitcoin"]["usd"]
    prices["eth"] = crypto_data["ethereum"]["usd"]

    return prices

def main():
    print(get_prices())

if __name__ == "__main__":
    main()
