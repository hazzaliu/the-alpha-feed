import os
from dotenv import load_dotenv

load_dotenv()

# Core Discord & API Keys
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

# Emperor's Court specific
EMPEROR_USER_ID = os.getenv("EMPEROR_USER_ID", "")  # Discord user ID of the Emperor

# Optional: Web search API for Court Herald and Royal Envoy
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# Legacy configs (kept for backwards compatibility if needed)
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
SCHEDULE_PRE_MARKET_UTC = {"hour": 13, "minute": 0}
SCHEDULE_POST_MARKET_UTC = {"hour": 22, "minute": 0}
RSS_FEEDS = []
NEWSAPI_QUERIES = []
