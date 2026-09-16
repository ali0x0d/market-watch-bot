# Market Watch Bot

A small Telegram bot that posts an hourly market snapshot to a channel: Bitcoin, Ethereum, gold, silver, crude oil, and the USDT/IRT rate.

## What it posts

At the top of every hour (in the configured timezone) the bot sends a message like:

```
🕒 2026-09-16 05:00

₿  BTC:     $75,839
⟠  ETH:     $2,403

🥇 Gold:    $4,327
🥈 Silver:  $64.33
🛢️ Oil:     $104.97

💵 USDT:    231,320 IRT
```

## Data sources

| Asset | Source | Symbol / ID |
|---|---|---|
| BTC, ETH | [CoinGecko](https://www.coingecko.com/en/api) | `bitcoin`, `ethereum` |
| Gold | CoinGecko (via [PAX Gold](https://paxos.com/paxgold/)) | `pax-gold` |
| Silver | Yahoo Finance ([yfinance](https://github.com/ranaroussi/yfinance)) | `SI=F` |
| Crude oil (WTI) | Yahoo Finance (yfinance) | `CL=F` |
| USDT / IRT | [Nobitex](https://nobitex.ir/) | `usdt-rls` |

Nobitex reports the USDT price in rials; the bot divides by 10 to display it in toman (IRT).

All three sources are fetched concurrently before each message is sent.

## Requirements

- Python 3.9+ (developed on 3.12)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- The bot added to the target channel as an administrator with permission to post

## Setup

```bash
git clone git@github.com:ali0x0d/market-watch-bot.git
cd market-watch-bot

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
BOT_TOKEN=123456789:your-bot-token
CHANNEL_ID=@your_channel        # or a numeric ID such as -1001234567890
BOT_TZ=Asia/Tehran              # optional, defaults to Asia/Tehran
```

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | yes | Telegram bot token |
| `CHANNEL_ID` | yes | Channel username (`@name`) or numeric chat ID to post to |
| `BOT_TZ` | no | IANA timezone used for scheduling and the message timestamp |

## Running

```bash
python main.py
```

The bot sleeps until the next full hour, fetches prices, posts the message, and repeats. It runs indefinitely, so in production run it under a process manager such as `systemd` or `pm2`.

## Deployment

Pushing to `main` triggers the [Deploy to Production](.github/workflows/deploy-production.yml) GitHub Actions workflow, which SSHes into the production server and runs `./deploy.sh` there. The deploy script lives on the server, not in this repository.

The workflow expects these repository secrets:

| Secret | Description |
|---|---|
| `HOST` | Server hostname or IP |
| `USERNAME` | SSH user |
| `KEY` | SSH private key |
| `PORT` | SSH port |
| `FINGERPRINT` | SSH host key fingerprint |

## Project structure

```
main.py           # scheduling loop, message formatting, Telegram sending
market_data.py    # price fetchers for CoinGecko, yfinance, and Nobitex
requirements.txt  # pinned dependencies
.github/workflows/deploy-production.yml
```

## License

This project is licensed under the [MIT License](LICENSE).
