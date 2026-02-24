# 🚀 Deploy The Emperor's Court (7 Bots)

## What Changed

Your court now runs **7 separate Discord bots simultaneously** — one for each courtier. Each bot:
- Has its own Discord identity and @mention
- Responds only when directly @mentioned
- Can participate in debates together
- Has a unique Gen Z personality

## Railway Deployment Steps

### 1. Update Environment Variables

Go to your Railway project → Variables tab and add these **7 new tokens** (use the actual tokens from your Discord Developer Portal):

```
LORD_SEBASTIAN_TOKEN=<your_lord_sebastian_token>
LADY_BEATRICE_TOKEN=<your_lady_beatrice_token>
LORD_EDMUND_TOKEN=<your_lord_edmund_token>
LADY_ARABELLA_TOKEN=<your_lady_arabella_token>
LADY_PHILIPPA_TOKEN=<your_lady_philippa_token>
LORD_ALISTAIR_TOKEN=<your_lord_alistair_token>
LADY_GENEVIEVE_TOKEN=<your_lady_genevieve_token>
```

**Note**: You already have these tokens from when you created the 7 bots. Copy them from your Discord Developer Portal or from your local `.env` file.

**Important**: Keep your existing variables (`OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `EMPEROR_USER_ID`). Just add these 7 new ones.

### 2. Push Code to GitHub

```bash
git add -A
git commit -m "Implement 7 separate courtier bots with individual @mentions"
git push origin main
```

Railway will automatically detect the push and redeploy.

### 3. Wait for Deployment

- Railway will build and start the app
- Watch the logs: you should see 7 bots come online
- Expected log output:
  ```
  [main] Starting 7 courtier bots...
  [main] The Emperor's Court is assembling...
  [Lord Sebastian] Online and ready to serve His Imperial Majesty
  [Lady Beatrice] Online and ready to serve His Imperial Majesty
  [Lord Edmund] Online and ready to serve His Imperial Majesty
  ...
  ```

### 4. Test in Discord

Once deployed, you'll see **7 bots appear online** in your Discord server:

1. **Lord Sebastian, Grand Architect** 👨
2. **Lady Beatrice, Treasurer of the Imperial Coffers** 👩
3. **Lord Edmund, Court Herald** 👨
4. **Lady Arabella, Royal Envoy** 👩
5. **Lady Philippa, Grand Vizier** 👩
6. **Lord Alistair, Royal Sage** 👨
7. **Lady Genevieve, Court Jester** 👩

#### Test Commands

```
!court
```
Lists all courtiers (any bot can respond).

```
!status
```
Shows which bot is responding.

```
@Lord Sebastian help me build a landing page
```
Only Lord Sebastian will respond.

```
@Lady Beatrice what's our burn rate looking like?
```
Only Lady Beatrice will respond.

```
@Lord Edmund what's trending in AI right now?
```
Lord Edmund will search the web and report back.

#### Test Multiple Mentions

```
@Lord Sebastian @Lady Genevieve how should we design the onboarding flow?
```
Both bots will respond to the same message!

## How It Works

### Architecture

- **Single Process, 7 Bot Clients**: One Python process runs 7 Discord bot instances concurrently using `asyncio.gather()`
- **Shared State**: All bots share the same courtier logic, database, and debate engine
- **Individual Responses**: Each bot only responds when it's @mentioned
- **Debate Mode**: Bots can all participate in Discord threads together

### Code Changes

1. **`main.py`**: Completely rewritten to:
   - Create 7 separate `discord.Bot` instances
   - Run them all concurrently with `asyncio.gather()`
   - Each bot listens for @mentions of itself
   - Shared debate engine for cross-bot discussions

2. **`config.py`**: Added 7 new token environment variables

3. **`.env`**: Updated with all 7 bot tokens

## Troubleshooting

### If a bot doesn't appear online:

1. Check Railway logs for errors
2. Verify the token is correct in Railway variables
3. Ensure the bot has these intents enabled in Discord Developer Portal:
   - Server Members Intent
   - Message Content Intent
   - Presence Intent

### If a bot doesn't respond to @mentions:

1. Make sure you're @mentioning the bot directly (click on the bot name in Discord)
2. Check Railway logs to see if the bot received the message
3. Verify `EMPEROR_USER_ID` matches your Discord user ID

### If you see "Missing token" errors:

- One or more of the 7 token environment variables is not set in Railway
- Double-check all 7 tokens are added to Railway's Variables tab

## Cost Estimate

Running 7 bots simultaneously:
- **Railway**: Still free tier (all bots run in one process)
- **OpenAI API**: ~$0.01-0.05 per conversation (same as before)
- **Supabase**: Free tier (same as before)

No additional cost for running multiple bots!

## Next Steps

After deployment:
1. Test each courtier individually
2. Test multiple @mentions in one message
3. Try the `!summon` command for debates
4. Start building your product with your Gen Z royal court! 👑
