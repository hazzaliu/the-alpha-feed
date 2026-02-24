# Deployment Checklist for The Emperor's Court

Use this checklist to deploy the bot to Railway and verify everything works.

## Pre-Deployment Setup

### ✅ Step 1: Supabase Database Setup

1. Go to [supabase.com](https://supabase.com) and open your project
2. Navigate to **SQL Editor** (left sidebar)
3. Copy the contents of `db/schema.sql`
4. Paste into SQL Editor and click **Run**
5. Verify tables were created:
   - Go to **Table Editor**
   - You should see: `conversations`, `courtier_responses`, `project_context`
6. Copy your credentials:
   - Settings → API
   - Copy **Project URL** (SUPABASE_URL)
   - Copy **service_role** key (SUPABASE_KEY) — NOT the anon key

### ✅ Step 2: Discord Bot Configuration

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Select your application
3. Go to **Bot** section
4. **Privileged Gateway Intents** — Enable:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
5. Copy your bot token (click **Reset Token** if needed)
6. **Get your Discord User ID** (to become the Emperor):
   - In Discord, enable Developer Mode: Settings → Advanced → Developer Mode
   - Right-click your username anywhere → Copy User ID
   - Save this ID for later

### ✅ Step 3: OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy it immediately (you won't see it again)

### ✅ Step 4: Optional - Web Search Setup

**For Court Herald and Royal Envoy to access real-time web data:**

1. Go to [tavily.com](https://tavily.com)
2. Sign up for free account
3. Copy your API key
4. If you skip this, courtiers will still work but won't have web search

## Deployment to Railway

### ✅ Step 5: Push to GitHub

```bash
cd /path/to/OpenClawEmpire

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Emperor's Court - Initial deployment"

# Add your GitHub remote (create the repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/emperors-court.git

# Push
git push -u origin main
```

**IMPORTANT**: Make sure `.env` is listed in `.gitignore` (it already is). Never commit your API keys!

### ✅ Step 6: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Authorize Railway to access your GitHub
5. Select the `emperors-court` repository
6. Railway will auto-detect the `Procfile` and start building

### ✅ Step 7: Configure Environment Variables

1. In Railway, click on your service
2. Go to **Variables** tab
3. Click **Raw Editor**
4. Paste all your environment variables:

```env
DISCORD_TOKEN=your_actual_discord_token
OPENAI_API_KEY=your_actual_openai_key
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_actual_supabase_service_key
EMPEROR_USER_ID=your_discord_user_id
TAVILY_API_KEY=your_tavily_key_if_you_have_it
```

5. Click **Update Variables**
6. Railway will automatically redeploy with the new variables

### ✅ Step 8: Monitor Deployment

1. In Railway, go to **Deployments** tab
2. Click on the active deployment
3. Watch the build logs
4. Look for:
   - `The Emperor's Court is assembled`
   - `Courtiers ready: The Grand Architect, The Royal Treasurer, ...`
5. If you see errors, check:
   - Environment variables are set correctly
   - Python version matches `runtime.txt` (3.12)
   - All dependencies installed from `requirements.txt`

## Post-Deployment Testing

### ✅ Step 9: Basic Health Check

In your Discord server, run these commands:

1. **Test bot is online:**
   ```
   !status
   ```
   Expected: Bot responds with "The Emperor's Court is assembled" message

2. **List courtiers:**
   ```
   !court
   ```
   Expected: Bot lists all 7 courtiers with their roles

### ✅ Step 10: Test Individual Courtiers

Test each courtier with a simple question:

1. **Grand Architect:**
   ```
   @Grand Architect should I use React or Vue?
   ```
   Expected: Technical response in Gen Z voice

2. **Royal Treasurer:**
   ```
   @Royal Treasurer is $20/month good pricing?
   ```
   Expected: Financial analysis with numbers

3. **Court Herald:**
   ```
   @Court Herald what's trending in AI?
   ```
   Expected: Searches web (if Tavily configured) and reports trends

4. **Royal Envoy:**
   ```
   @Royal Envoy how do I launch a product?
   ```
   Expected: GTM strategy response

5. **Grand Vizier:**
   ```
   @Grand Vizier I want to build a todo app
   ```
   Expected: Asks clarifying questions

6. **Royal Sage:**
   ```
   @Royal Sage should I add social features?
   ```
   Expected: Strategic analysis

7. **Court Jester:**
   ```
   @Court Jester is this UI too complex?
   ```
   Expected: UX critique

### ✅ Step 11: Test Debate Mode

```
!summon Should we build a mobile app or web app first?
```

Expected:
- Bot creates a Discord thread
- Grand Vizier opens the debate
- Multiple courtiers participate (Architect, Sage, Jester)
- Discussion happens in the thread
- Vizier synthesizes conclusion

### ✅ Step 12: Verify Database Storage

1. Go back to Supabase → Table Editor
2. Check `conversations` table — should have new rows for each interaction
3. Check `courtier_responses` table — should have responses from each courtier

## Troubleshooting

### Bot doesn't respond at all
- Check Railway logs for errors
- Verify `DISCORD_TOKEN` is correct (regenerate if needed)
- Verify Discord intents are enabled (Message Content, Server Members)

### "Only the Emperor can command" message
- You set `EMPEROR_USER_ID` but it doesn't match your Discord user ID
- Double-check you copied YOUR user ID (right-click your name → Copy User ID)
- Or remove `EMPEROR_USER_ID` from Railway variables to allow everyone (for testing)

### Courtiers respond but database errors
- Check `SUPABASE_KEY` — must be **service_role** key, not anon key
- Check `SUPABASE_URL` format: `https://xxxxx.supabase.co`
- Run `db/schema.sql` again in Supabase SQL Editor

### Court Herald/Royal Envoy can't search web
- This is fine if you didn't configure `TAVILY_API_KEY`
- They'll still respond, just without real-time web data
- To enable: sign up at tavily.com, add key to Railway variables

### OpenAI errors
- Check `OPENAI_API_KEY` is valid
- Check OpenAI account has credits/billing set up
- OpenAI may rate-limit free accounts

## Success Criteria

✅ All 7 courtiers respond to @mentions
✅ Each courtier has distinct Gen Z personality
✅ Debate mode creates threads and coordinates courtiers
✅ Database stores conversations and responses
✅ Web search works for Herald & Envoy (if configured)
✅ Only Emperor can command (if EMPEROR_USER_ID is set)

---

Once all tests pass, The Emperor's Court is fully operational! 👑

Use `!court` anytime to see all available courtiers, and @mention them whenever you need their expertise.
