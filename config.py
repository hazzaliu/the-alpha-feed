import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

SCHEDULE_PRE_MARKET_UTC = {"hour": 13, "minute": 0}   # 8:00 AM ET
SCHEDULE_POST_MARKET_UTC = {"hour": 22, "minute": 0}  # 5:00 PM ET

RSS_FEEDS = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",        # CNBC US Markets
    "https://www.cnbc.com/id/10000664/device/rss/rss.html",         # CNBC Tech
    "https://feeds.reuters.com/reuters/businessNews",                # Reuters Business
    "https://www.coindesk.com/arc/outboundfeeds/rss/",              # CoinDesk Crypto
    "https://cointelegraph.com/rss",                                 # CoinTelegraph
]

NEWSAPI_QUERIES = [
    "US stock market",
    "S&P 500 nasdaq",
    "cryptocurrency bitcoin ethereum",
    "Federal Reserve interest rates",
    "inflation CPI earnings",
]
