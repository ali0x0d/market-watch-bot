import requests

def get_prices():
    crypto_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd").json()
    btc = crypto_data["bitcoin"]["usd"]
    eth = crypto_data["ethereum"]["usd"]

    return btc, eth

def main():
    print(get_prices())

if __name__ == "__main__":
    main()
