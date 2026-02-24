# 🎉 What's New — 7 Separate Bots!

## The Big Change

Your Emperor's Court now runs **7 separate Discord bots** instead of 1 bot with internal agents.

### Before (Old System)
- 1 Discord bot
- Internal routing to different "agents"
- Had to type keywords like "architect" or "treasurer"
- Bot would guess which courtier you wanted

### After (New System)
- **7 Discord bots** — one for each courtier
- Each bot has its own Discord identity
- Direct @mentions: `@Lord Sebastian`, `@Lady Beatrice`, etc.
- No guessing — you choose exactly who responds
- Multiple bots can respond to the same message

## Your 7 Courtiers

Each is now a **separate Discord bot** you can @mention:

1. **@Lord Sebastian, Grand Architect** (Seb) — Engineering & Code
2. **@Lady Beatrice, Treasurer of the Imperial Coffers** (Bea) — Finance & Business
3. **@Lord Edmund, Court Herald** (Eddie) — News & Intelligence (web search enabled)
4. **@Lady Arabella, Royal Envoy** (Bella) — Marketing & GTM (web search enabled)
5. **@Lady Philippa, Grand Vizier** (Pippa) — Coordination & Planning
6. **@Lord Alistair, Royal Sage** (Ali) — Strategy & Product Vision
7. **@Lady Genevieve, Court Jester** (Genny) — UX & User Experience

## How to Use

### Single Courtier
```
@Lord Sebastian should I use React or Vue?
```
Only Lord Sebastian responds.

### Multiple Courtiers
```
@Lord Sebastian @Lady Genevieve how should we design the signup flow?
```
Both respond to the same message!

### Commands (any bot can handle these)
```
!court          → List all courtiers
!status         → Check if courtiers are online
!summon [topic] → Start a debate with multiple courtiers
```

## Technical Details

### Code Changes

**`main.py`** — Completely rewritten:
- Creates 7 separate `discord.Bot` instances
- Runs them all concurrently with `asyncio.gather()`
- Each bot listens for @mentions of itself
- Shared state for debates and database

**`config.py`** — Added 7 token variables:
- `LORD_SEBASTIAN_TOKEN`
- `LADY_BEATRICE_TOKEN`
- `LORD_EDMUND_TOKEN`
- `LADY_ARABELLA_TOKEN`
- `LADY_PHILIPPA_TOKEN`
- `LORD_ALISTAIR_TOKEN`
- `LADY_GENEVIEVE_TOKEN`

**`.env`** — Updated with all 7 tokens

### Architecture

```
Single Railway Process
    ↓
Runs 7 Discord bot clients concurrently
    ↓
Each bot listens for @mentions
    ↓
Shared database, debate engine, courtier logic
```

**Benefits:**
- No additional cost (still one process)
- Better UX (direct @mentions)
- Clearer communication (you see who's talking)
- More Discord-native (bots appear in member list)

## Deploy Steps

See [`DEPLOY_CHECKLIST.md`](DEPLOY_CHECKLIST.md) for the full guide.

**TL;DR:**
1. Push code to GitHub
2. Add 7 new token variables to Railway
3. Railway auto-deploys
4. See 7 bots come online in Discord
5. Start @mentioning them!

## Why This Is Better

1. **Clarity**: You see exactly who's responding (bot username shows in Discord)
2. **Control**: Direct @mentions mean no ambiguity
3. **Discord Native**: Bots appear in member list, have avatars, online status
4. **Multi-Response**: Multiple bots can respond to one message
5. **Scalable**: Easy to add more courtiers later

Your court is now a true royal assembly! 👑
