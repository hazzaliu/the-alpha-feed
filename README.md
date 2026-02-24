# The Emperor's Court 👑

A multi-agent Discord bot system where specialized Gen Z-speaking courtiers help you build products. Each courtier is an AI agent with distinct personality and domain expertise, reporting directly to you, the Emperor.

## The Royal Dynasty (4 Ladies, 3 Lords)

| Courtier | Role | Specialty | Vibe |
|---|---|---|---|
| **Lord Architect** (He/Him) | Chief Engineer & Technical Advisor | Code review, architecture, tech stack, debugging | 3am coder energy, "skill issue" |
| **Lady Treasurer** (She/Her) | CFO & Deal Analyzer | Pricing, costs, unit economics, fundraising | Spreadsheet queen, That Girl |
| **Lord Herald** (He/Him) | Chief Intelligence Officer | Product trends, competitor intel, market news (web search) | Chronically online, "I called it" |
| **Lady Envoy** (She/Her) | Marketing & Growth Strategist | GTM, distribution, viral mechanics, growth (web search) | Content creator energy, "blow up" |
| **Lady Vizier** (She/Her) | Chief of Staff & Coordinator | Requirement gathering, task breakdown, coordinating courtiers | Notion girlie, organized bestie |
| **Lord Sage** (He/Him) | Chief Product Officer | Product strategy, roadmap, prioritization, long-term vision | Thinks 10 steps ahead, chess player |
| **Lady Jester** (She/Her) | Chief Experience Officer | UX review, usability, accessibility, user advocacy | Brutally honest, "users gonna bounce" |

## Commands

- `!court` — list all courtiers and their roles
- `!summon [topic]` — start a court debate with multiple courtiers
- `!status` — check if the court is assembled
- `@[Courtier Name] [your question]` — speak directly to a specific courtier

### Example Usage

```
@Lord Architect should I use PostgreSQL or MongoDB?
@Lady Treasurer is $29/month good pricing for a SaaS?
@Lord Herald what's trending in AI productivity tools?
@Lady Vizier I want to build a landing page
!summon Should we add social features to our app?
```

---

## Deployment on Railway (zero local machine involvement)

### Step 1 — Supabase Setup

1. Go to [supabase.com](https://supabase.com) and open your project
2. Go to **SQL Editor** and run the schema from [`db/schema.sql`](db/schema.sql)
3. This creates tables for conversations, courtier responses, and project context

### Step 2 — Discord Bot Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Select your application → Bot
3. Enable these **Privileged Gateway Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
4. Copy your bot token
5. **Get your Discord User ID** (to become the Emperor):
   - Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
   - Right-click your username → Copy User ID

### Step 3 — Optional: Web Search Setup (for Court Herald & Royal Envoy)

The Court Herald and Royal Envoy can perform real-time web searches to stay current on trends, competitors, and market intelligence.

**Option A: Tavily API (Recommended)**
1. Go to [tavily.com](https://tavily.com) and sign up
2. Get your API key (free tier available)
3. Add `TAVILY_API_KEY` to your environment variables

**Option B: Skip web search**
- If you don't configure a search API, courtiers will still work but won't have real-time web data

### Step 4 — Push to GitHub

```bash
git init
git add .
git commit -m "The Emperor's Court initial commit"
git remote add origin https://github.com/YOUR_USERNAME/emperors-court.git
git push -u origin main
```

> **Important:** `.env` is in `.gitignore` — your keys will NOT be pushed to GitHub.

### Step 5 — Deploy on Railway

1. Go to [railway.app](https://railway.app) and create a new project
2. Choose **Deploy from GitHub repo** → select your repo
3. Railway will detect the `Procfile` automatically
4. Go to your service → **Variables** tab → add all environment variables:

| Variable | Value | Required? |
|---|---|---|
| `DISCORD_TOKEN` | Your Discord bot token | ✅ Required |
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Required |
| `SUPABASE_URL` | `https://your-project-id.supabase.co` | ✅ Required |
| `SUPABASE_KEY` | Your Supabase secret key (not anon key) | ✅ Required |
| `EMPEROR_USER_ID` | Your Discord user ID | ✅ Required (or bot responds to everyone) |
| `TAVILY_API_KEY` | Your Tavily API key | Optional (enables web search) |

5. Click **Deploy** — Railway will build and run the bot entirely on their servers

### Step 6 — Verify

In your Discord server:
1. Type `!status` — the bot should confirm the court is assembled
2. Type `!court` — see all 7 courtiers
3. Try `@Grand Architect hello` — the Grand Architect should respond in Gen Z voice

---

## Architecture

```
Emperor (You)
    ↓
@mentions specific courtier
    ↓
Courtier responds (using OpenAI with personality prompt)
    ↓
Response saved to Supabase
```

### Debate Mode

When you use `!summon [topic]`, the Grand Vizier creates a Discord thread and coordinates multiple courtiers to discuss the topic. They debate, share perspectives, and the Vizier synthesizes a conclusion.

---

## Cost Estimate (monthly)

- Railway: Free tier or $5/month Hobby plan
- OpenAI: ~$10-30/month (depends on usage, multi-bot debates use more tokens)
- Supabase: Free tier
- Tavily API: Free tier (1000 searches/month) or $10-20/month
- **Total: $10-55/month**

---

## How It Works

Each courtier is:
1. A Python class inheriting from `BaseCourtier`
2. Loaded with a detailed Gen Z personality prompt
3. Uses OpenAI's `gpt-4o` model for responses
4. Has unique speech patterns, catchphrases, and expertise

The dispatcher in `main.py`:
- Listens for @mentions of courtier names
- Routes messages to the correct courtier
- Handles web search for Herald & Envoy
- Saves all conversations to Supabase
- Coordinates multi-courtier debates via Discord threads

---

## File Structure

```
emperors-court/
├── main.py                      # Discord bot + dispatcher
├── courtiers/                   # All courtier classes
│   ├── grand_architect.py
│   ├── royal_treasurer.py
│   ├── court_herald.py
│   ├── royal_envoy.py
│   ├── grand_vizier.py
│   ├── royal_sage.py
│   └── court_jester.py
├── prompts/                     # Personality prompts for each courtier
│   ├── grand_architect.txt
│   ├── royal_treasurer.txt
│   └── ... (7 total)
├── services/
│   ├── web_search.py           # Tavily API integration
│   ├── debate_engine.py        # Multi-courtier debates in threads
│   └── context_manager.py      # Supabase storage
├── db/
│   ├── schema.sql              # Supabase schema
│   └── supabase_client.py      # Database client
├── config.py
├── requirements.txt
├── Procfile                     # Railway deployment config
└── runtime.txt                  # Python version
```

---

## Customization

### Add a New Courtier

1. Create a new class in `courtiers/` inheriting from `BaseCourtier`
2. Write a personality prompt in `prompts/`
3. Add detection logic in `main.py`'s `detect_courtier_mention()`
4. Add to `courtiers` dict in `main.py`

### Change Personalities

Edit the prompt files in `prompts/` to adjust tone, speech patterns, or expertise. The LLM will adapt to the new personality immediately.

### Restrict to Emperor Only

Set `EMPEROR_USER_ID` environment variable to your Discord user ID. Only you will be able to command the court.

---

*The court awaits your command, Your Majesty* 🙇
