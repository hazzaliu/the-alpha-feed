# The Alpha Feed 💅

A multi-agent Discord bot that drops daily US equities + crypto market breakdowns in full Gen Z voice.

## The Cast

| Character | Role |
|---|---|
| **The Plug** | Fetches headlines from NewsAPI + RSS |
| **That Girl** | Financial analyst — does the actual research |
| **The Bestie** | Fact-checker — calls out anything sus |
| **The Group Chat** | Gen Z translator — makes it actually readable |
| **The Content Creator** | Discord formatter — makes it look aesthetic |
| **The Girlboss** | Orchestrator — runs the whole operation |

## Commands

- `!drop the alpha` — manually trigger a drop
- `!drop post` — trigger a post-market drop
- `!status` — check if the bot is alive

## Automated Schedule

- **8:00 AM ET** — pre-market drop (daily)
- **5:00 PM ET** — post-market drop (daily)

---

## Deployment on Railway (zero local machine involvement)

### Step 1 — Supabase Setup

1. Go to [supabase.com](https://supabase.com) and open your project
2. Go to **SQL Editor** and run this schema:

```sql
create table if not exists seen_headlines (
    id bigserial primary key,
    url_hash text not null unique,
    url text not null,
    title text,
    seen_at timestamptz not null default now()
);

create table if not exists drops (
    id bigserial primary key,
    raw_json jsonb,
    final_text text,
    created_at timestamptz not null default now()
);
```

### Step 2 — Discord Bot Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Select your application → Bot
3. Enable **Message Content Intent** under Privileged Gateway Intents
4. Copy your bot token

### Step 3 — Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/the-alpha-feed.git
git push -u origin main
```

> **Important:** `.env` is in `.gitignore` — your keys will NOT be pushed to GitHub.

### Step 4 — Deploy on Railway

1. Go to [railway.app](https://railway.app) and create a new project
2. Choose **Deploy from GitHub repo** → select your repo
3. Railway will detect the `Procfile` automatically
4. Go to your service → **Variables** tab → add all environment variables:

| Variable | Value |
|---|---|
| `DISCORD_TOKEN` | your Discord bot token |
| `DISCORD_CHANNEL_ID` | your Discord channel ID |
| `OPENAI_API_KEY` | your OpenAI API key |
| `NEWSAPI_KEY` | your NewsAPI.org key |
| `SUPABASE_URL` | `https://your-project-id.supabase.co` |
| `SUPABASE_KEY` | your Supabase secret key |

5. Click **Deploy** — Railway will build and run the bot entirely on their servers

### Step 5 — Verify

In your Discord server, type `!status` — the bot should respond confirming it's live.

---

## Cost Estimate (monthly)

- Railway: Free tier or $5/month Hobby plan
- OpenAI: ~$2-8/month
- Supabase: Free tier
- NewsAPI: Free tier (100 req/day)
- **Total: $0-13/month**

---

*This bot is for educational purposes only and does not constitute financial advice.*
