import os
from dotenv import load_dotenv

load_dotenv()

# Core API Keys
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

# Emperor's Court specific
EMPEROR_USER_ID = os.getenv("EMPEROR_USER_ID", "")  # Discord user ID of the Emperor

# 7 Courtier Bot Tokens
LORD_SEBASTIAN_TOKEN = os.getenv("LORD_SEBASTIAN_TOKEN", "")
LADY_BEATRICE_TOKEN = os.getenv("LADY_BEATRICE_TOKEN", "")
LORD_EDMUND_TOKEN = os.getenv("LORD_EDMUND_TOKEN", "")
LADY_ARABELLA_TOKEN = os.getenv("LADY_ARABELLA_TOKEN", "")
LADY_PHILIPPA_TOKEN = os.getenv("LADY_PHILIPPA_TOKEN", "")
LORD_ALISTAIR_TOKEN = os.getenv("LORD_ALISTAIR_TOKEN", "")
LADY_GENEVIEVE_TOKEN = os.getenv("LADY_GENEVIEVE_TOKEN", "")

# Optional: Web search API for Lord Edmund and Lady Arabella
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# Legacy configs (kept for backwards compatibility)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")  # Old single bot token
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
SCHEDULE_PRE_MARKET_UTC = {"hour": 13, "minute": 0}
SCHEDULE_POST_MARKET_UTC = {"hour": 22, "minute": 0}
RSS_FEEDS = []
NEWSAPI_QUERIES = []
