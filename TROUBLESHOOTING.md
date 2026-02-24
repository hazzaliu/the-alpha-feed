# 🔧 Troubleshooting Guide

## Common Issues & Fixes

### 1. "Missing token" Error in Railway Logs

**Symptoms:**
```
[ERROR] Missing token for lord_sebastian
[ERROR] Missing token for lady_beatrice
...
[FATAL] Cannot start. Missing 7 tokens
```

**Fix:**
You haven't added the 7 bot tokens to Railway yet!

1. Open `RAILWAY_TOKENS.txt` (in this folder)
2. Go to Railway → Your Project → Variables
3. For each line, add a new variable:
   - Variable name: `LORD_SEBASTIAN_TOKEN`
   - Value: (paste the token)
4. Repeat for all 7 tokens
5. Railway will auto-redeploy

### 2. "401 Unauthorized" or "Improper token" Error

**Symptoms:**
```
discord.errors.HTTPException: 401 Unauthorized
discord.errors.LoginFailure: Improper token has been passed
```

**Fix:**
One or more tokens are invalid or expired.

1. Go to Discord Developer Portal
2. For each bot, go to Bot → Reset Token
3. Copy the new token
4. Update in Railway Variables
5. Redeploy

### 3. "PrivilegedIntentsRequired" Error

**Symptoms:**
```
discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents
```

**Fix:**
You need to enable intents for ALL 7 bots.

For each bot in Discord Developer Portal:
1. Go to Bot → Privileged Gateway Intents
2. Enable:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent (optional but recommended)
3. Save changes
4. Redeploy on Railway

### 4. Bots Online But Not Responding

**Symptoms:**
- 7 bots show as online in Discord
- But don't respond when @mentioned

**Possible causes:**

**A) Wrong User ID**
- Check Railway logs for: `Serving Emperor ID: XXXXXXX`
- Compare with your Discord user ID
- If different, update `EMPEROR_USER_ID` in Railway

**B) Not Actually @Mentioning**
- Make sure you're clicking the bot name to @mention
- Should look like: `@Lord Sebastian` (blue/highlighted)
- Not just typing "Lord Sebastian" in plain text

**C) Bots Not in Server**
- Check if all 7 bots are in your Discord server member list
- If missing, use the OAuth2 URL to invite them
- URL format: `https://discord.com/api/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=8&scope=bot`

### 5. Only Some Bots Online

**Symptoms:**
- 3 bots online, 4 offline
- Or only 1 bot online

**Fix:**
Check Railway logs to see which bots failed to start. Look for error messages like:

```
[Lord Sebastian] Online and ready ✓
[Lady Beatrice] Online and ready ✓
[ERROR] Failed to start lord_edmund: ...
```

Then fix the specific bot's token in Railway Variables.

### 6. "Module not found" Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'discord'
ModuleNotFoundError: No module named 'openai'
```

**Fix:**
Railway didn't install dependencies properly.

1. Check that `requirements.txt` exists in your repo
2. Check that `runtime.txt` exists with `3.12`
3. Trigger a manual redeploy in Railway
4. Check build logs to ensure `pip install` succeeded

### 7. Database Errors

**Symptoms:**
```
[Lord Sebastian] Database save error: ...
```

**Fix:**
Check your Supabase credentials:
1. Verify `SUPABASE_URL` is correct in Railway
2. Verify `SUPABASE_KEY` is the **service role key** (not anon key)
3. Verify tables exist (run `db/schema.sql` in Supabase SQL Editor)

### 8. Web Search Not Working (Lord Edmund, Lady Arabella)

**Symptoms:**
- Lord Edmund or Lady Arabella respond but don't include web search results
- Or error messages about Tavily API

**Fix:**
Web search is optional. If you want it:
1. Get API key from [tavily.com](https://tavily.com)
2. Add `TAVILY_API_KEY` to Railway Variables
3. Redeploy

If you don't need web search, ignore this — bots will still work!

## How to Debug

### Step 1: Check Railway Logs

Railway → Your Project → Deployments → Latest → Logs

Look for:
- `[main] Starting 7 courtier bots...` — startup message
- `[Lord Sebastian] Online and ready...` — each bot coming online
- Any `[ERROR]` or `[FATAL]` messages

### Step 2: Check Discord

- Are the 7 bots in your server member list?
- Are they online (green status)?
- Try `!status` — does any bot respond?

### Step 3: Test @Mentions

Try each bot individually:
```
@Lord Sebastian hello
@Lady Beatrice hello
@Lord Edmund hello
@Lady Arabella hello
@Lady Philippa hello
@Lord Alistair hello
@Lady Genevieve hello
```

Note which ones respond and which don't.

### Step 4: Check Railway Variables

Railway → Variables tab

Verify you have:
- `LORD_SEBASTIAN_TOKEN` ✓
- `LADY_BEATRICE_TOKEN` ✓
- `LORD_EDMUND_TOKEN` ✓
- `LADY_ARABELLA_TOKEN` ✓
- `LADY_PHILIPPA_TOKEN` ✓
- `LORD_ALISTAIR_TOKEN` ✓
- `LADY_GENEVIEVE_TOKEN` ✓
- `OPENAI_API_KEY` ✓
- `SUPABASE_URL` ✓
- `SUPABASE_KEY` ✓
- `EMPEROR_USER_ID` ✓

## Still Stuck?

Share the Railway logs (the part that says `$ python main.py` and below) and I'll help debug!

Look for:
- Error messages
- Stack traces
- Which bots started successfully
- Which bots failed
