# 🤖 Creating 7 Separate Discord Bots - Step by Step

## 👑 Your British Royal Court

You'll create 7 Discord bot applications, one for each courtier. Each will have their own account, avatar, and personality!

---

## 📋 The 7 Bots to Create

| # | Bot Application Name | Discord Username | Nickname |
|---|---|---|---|
| 1 | Lord Sebastian, Grand Architect | `Lord Sebastian, Grand Architect` | Seb |
| 2 | Lady Beatrice, Royal Treasurer | `Lady Beatrice, Royal Treasurer` | Bea |
| 3 | Lord Edmund, Court Herald | `Lord Edmund, Court Herald` | Eddie |
| 4 | Lady Arabella, Royal Envoy | `Lady Arabella, Royal Envoy` | Bella |
| 5 | Lady Philippa, Grand Vizier | `Lady Philippa, Grand Vizier` | Pippa |
| 6 | Lord Alistair, Royal Sage | `Lord Alistair, Royal Sage` | Ali |
| 7 | Lady Genevieve, Court Jester | `Lady Genevieve, Court Jester` | Genny |

---

## 🔧 For EACH Bot (Repeat 7 Times)

### Step 1: Create Discord Application

1. Go to: https://discord.com/developers/applications
2. Click **New Application**
3. **Name:** Use the exact name from the table above (e.g., "Lord Sebastian, Grand Architect")
4. Click **Create**

### Step 2: Configure the Bot

1. Click **Bot** in left sidebar
2. Click **Add Bot** → Confirm
3. **Username:** Should auto-fill with application name (keep it)
4. **Icon/Avatar:** (Optional but recommended)
   - Upload an avatar that matches their personality
   - Ideas below in the Avatar Guide section
5. **Privileged Gateway Intents** - Enable ALL three:
   - ✅ Presence Intent
   - ✅ Server Members Intent  
   - ✅ Message Content Intent
6. Click **Reset Token** button
7. **COPY THE TOKEN** - Save it somewhere safe!
8. Click **Save Changes**

### Step 3: Generate Invite URL

1. Click **OAuth2** → **URL Generator** in left sidebar
2. **Scopes:** Check `bot`
3. **Bot Permissions:** Check these:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Send Messages in Threads
   - ✅ Create Public Threads
   - ✅ Read Message History
   - ✅ Add Reactions
4. **Copy the generated URL** at the bottom
5. Open URL in new browser tab
6. Select your Discord server
7. Click **Authorize**
8. Complete the captcha
9. Bot is now in your server!

### Step 4: Save the Token

After creating each bot, save its token in this format:

```
LORD_SEBASTIAN_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LADY_BEATRICE_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LORD_EDMUND_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LADY_ARABELLA_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LADY_PHILIPPA_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LORD_ALISTAIR_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
LADY_GENEVIEVE_TOKEN=MTQ3NTYyODk0NzIzNTU0MTI3Nw.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxx
```

---

## 🎨 Avatar/Icon Ideas (Optional but Fun)

### Lord Sebastian (Grand Architect)
- Dark mode aesthetic
- Terminal/code editor screenshot
- Hoodie silhouette
- Coffee + laptop
- Color: Dark blue, green (terminal colors)

### Lady Beatrice (Royal Treasurer)
- Spreadsheet screenshot
- Calculator
- Coffee cup + laptop
- Business casual aesthetic
- Color: Gold, green (money colors)

### Lord Edmund (Court Herald)
- Phone with notifications
- Twitter/social media icons
- News ticker aesthetic
- RSS feed icon
- Color: Blue (Twitter blue), red (news alert)

### Lady Arabella (Royal Envoy)
- Ring light
- Camera/content creator setup
- Aesthetic gradient
- Social media icons
- Color: Pink, purple (influencer aesthetic)

### Lady Philippa (Grand Vizier)
- Notion logo or planner
- Sticky notes
- Checklist
- Calendar
- Color: Pastel, organized aesthetic

### Lord Alistair (Royal Sage)
- Chess pieces
- Minimalist design
- Brain/thinking icon
- Strategic diagram
- Color: Purple, dark blue (wisdom colors)

### Lady Genevieve (Court Jester)
- Colorful design
- UI/UX tools (Figma)
- Playful aesthetic
- User icon
- Color: Bright, colorful, fun

---

## ⏱️ Time Estimate

- **Per bot:** ~3-4 minutes
- **Total for 7 bots:** ~20-30 minutes
- **Inviting all to server:** Already done as you create each one

---

## ✅ Checklist (Track Your Progress)

Create and invite each bot:

- [ ] 1. Lord Sebastian, Grand Architect (token saved)
- [ ] 2. Lady Beatrice, Royal Treasurer (token saved)
- [ ] 3. Lord Edmund, Court Herald (token saved)
- [ ] 4. Lady Arabella, Royal Envoy (token saved)
- [ ] 5. Lady Philippa, Grand Vizier (token saved)
- [ ] 6. Lord Alistair, Royal Sage (token saved)
- [ ] 7. Lady Genevieve, Court Jester (token saved)

---

## 🚨 Important Notes

1. **Save each token immediately** - you can't see it again after you navigate away
2. **Enable all 3 intents** for each bot (Presence, Server Members, Message Content)
3. **Invite each bot to your server** using the OAuth2 URL
4. **Don't share tokens publicly** - they're like passwords

---

## 🔄 After Creating All 7 Bots

Once you have all 7 tokens, send them to me in this format:

```
LORD_SEBASTIAN_TOKEN=your_token_here
LADY_BEATRICE_TOKEN=your_token_here
LORD_EDMUND_TOKEN=your_token_here
LADY_ARABELLA_TOKEN=your_token_here
LADY_PHILIPPA_TOKEN=your_token_here
LORD_ALISTAIR_TOKEN=your_token_here
LADY_GENEVIEVE_TOKEN=your_token_here
```

Then I'll:
1. Update the code to run all 7 bots simultaneously
2. Each bot will respond only to their own @mentions
3. They can all participate in debates together
4. Deploy to Railway with all 7 tokens

---

## 💡 Pro Tips

- **Do them in order** - easier to track which ones you've done
- **Use a text editor** - paste each token as you get it so you don't lose them
- **Test in Discord** - after inviting each bot, you'll see them in your member list (they'll be offline until we deploy)
- **Avatar consistency** - if you add avatars, keep a similar style for the whole court

---

**Start creating the bots now!** Let me know when you have all 7 tokens and I'll update the code to run them all! 👑
