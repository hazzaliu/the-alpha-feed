# 🚀 Deploy Checklist — 7 Bots Edition

## ✅ Pre-Deployment (Done)

- [x] Created 7 Discord bot applications
- [x] Enabled intents for all 7 bots
- [x] Invited all 7 bots to your Discord server
- [x] Got all 7 bot tokens
- [x] Updated code to run 7 bots simultaneously
- [x] Updated `.env` with all tokens

## 🎯 Deploy Now

### 1. Push to GitHub

```bash
cd /Users/admin/Desktop/OpenClawEmpire
git add -A
git commit -m "Implement 7 separate courtier bots"
git push origin main
```

### 2. Update Railway Variables

Go to Railway → Your Project → Variables

Add these **7 new variables** (copy the actual tokens from your local `.env` file):

```
LORD_SEBASTIAN_TOKEN=<paste_your_token_here>
LADY_BEATRICE_TOKEN=<paste_your_token_here>
LORD_EDMUND_TOKEN=<paste_your_token_here>
LADY_ARABELLA_TOKEN=<paste_your_token_here>
LADY_PHILIPPA_TOKEN=<paste_your_token_here>
LORD_ALISTAIR_TOKEN=<paste_your_token_here>
LADY_GENEVIEVE_TOKEN=<paste_your_token_here>
```

**Tip**: Open your local `.env` file and copy the tokens from there.

**Keep your existing variables** (`OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `EMPEROR_USER_ID`).

### 3. Wait for Deployment

Railway will automatically redeploy after you push to GitHub.

Watch the logs — you should see:
```
[main] Starting 7 courtier bots...
[Lord Sebastian] Online and ready to serve His Imperial Majesty
[Lady Beatrice] Online and ready to serve His Imperial Majesty
[Lord Edmund] Online and ready to serve His Imperial Majesty
[Lady Arabella] Online and ready to serve His Imperial Majesty
[Lady Philippa] Online and ready to serve His Imperial Majesty
[Lord Alistair] Online and ready to serve His Imperial Majesty
[Lady Genevieve] Online and ready to serve His Imperial Majesty
```

### 4. Test in Discord

You should see **7 bots online** in your server member list!

Try these:

```
!court
```

```
@Lord Sebastian yo what's good?
```

```
@Lady Beatrice help me price my product
```

```
@Lord Edmund what's trending in tech?
```

```
@Lady Genevieve is this UI too cluttered?
```

## 🎉 Success Criteria

- [ ] All 7 bots appear online in Discord
- [ ] Each bot responds when @mentioned
- [ ] `!court` command works
- [ ] `!status` command works
- [ ] Multiple bots can be @mentioned in one message

## 🔧 Troubleshooting

### Bot not appearing online?
- Check Railway logs for errors
- Verify token is correct in Railway variables
- Ensure intents are enabled in Discord Developer Portal

### Bot not responding?
- Make sure you're @mentioning the bot (click the name)
- Check Railway logs to see if message was received
- Verify `EMPEROR_USER_ID` matches your Discord ID

### "Missing token" error?
- One of the 7 tokens is not set in Railway
- Double-check all 7 are added to Variables tab

---

## What's Next?

Once deployed, start using your court:
- Ask Lord Sebastian for coding help
- Ask Lady Beatrice for financial advice
- Ask Lord Edmund for market trends
- Ask Lady Arabella for marketing strategies
- Ask Lady Philippa to coordinate your tasks
- Ask Lord Alistair for product strategy
- Ask Lady Genevieve for UX feedback

Your Gen Z royal court is ready to help you build! 👑
