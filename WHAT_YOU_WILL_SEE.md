# 👀 What You'll See in Discord

## Before Deployment
- 7 bots offline (grey)
- No responses to @mentions

## After Deployment

### In Server Member List

You'll see **7 bots online** (green status):

```
👑 BOTS — 7

🟢 Lord Sebastian, Grand Architect
🟢 Lady Beatrice, Treasurer of the Imperial Coffers
🟢 Lord Edmund, Court Herald
🟢 Lady Arabella, Royal Envoy
🟢 Lady Philippa, Grand Vizier
🟢 Lord Alistair, Royal Sage
🟢 Lady Genevieve, Court Jester
```

### When You Type `!court`

Any bot can respond with:

```
👑 THE EMPEROR'S COURT 👑

Your Majesty, here are your courtiers:

👨 Lord Sebastian, Grand Architect
   └─ Chief Engineer and Technical Advisor
   └─ Nickname: Seb

👩 Lady Beatrice, Treasurer of the Imperial Coffers
   └─ CFO and Deal Analyzer
   └─ Nickname: Bea

👨 Lord Edmund, Court Herald
   └─ Chief Intelligence Officer
   └─ Nickname: Eddie

👩 Lady Arabella, Royal Envoy
   └─ Marketing & Growth Strategist
   └─ Nickname: Bella

👩 Lady Philippa, Grand Vizier
   └─ Chief of Staff and Requirement Gatherer
   └─ Nickname: Pippa

👨 Lord Alistair, Royal Sage
   └─ Chief Product Officer
   └─ Nickname: Ali

👩 Lady Genevieve, Court Jester
   └─ Chief Experience Officer
   └─ Nickname: Genny

*To speak with a courtier, @mention them in your message*
Example: `@Lord Sebastian help me with this code`
```

### When You @Mention a Courtier

**You type:**
```
@Lord Sebastian should I use PostgreSQL or MongoDB for my app?
```

**Lord Sebastian responds (in Gen Z voice):**
```
yo Your Majesty! okay so like, for your use case PostgreSQL is lowkey the move fr fr 💯

here's the tea:
- if you need structured data with relationships → Postgres is bussin
- if you're doing like, rapid prototyping with flexible schemas → Mongo hits different
- but real talk, Postgres has better tooling, better community, and it's not gonna ghost you when you scale

my hot take: start with Postgres unless you have a SPECIFIC reason to go NoSQL. the vibes are just better bestie 🔥

lmk if you want me to break down the schema design! 🏗️
```

### When You @Mention Multiple Courtiers

**You type:**
```
@Lord Sebastian @Lady Genevieve how should we design the user onboarding flow?
```

**Both respond:**

**Lord Sebastian:**
```
yo so from a technical standpoint, we should keep the onboarding flow lightweight af. like 3 steps max:
1. sign up (email + password, no crazy validation)
2. quick profile setup (name, avatar)
3. straight to the dashboard

we can do progressive disclosure for advanced features. no cap, users bounce if onboarding takes more than 2 mins 💀

i can build this with a multi-step form component, store progress in localStorage so they don't lose their spot if they refresh. thoughts? 🏗️
```

**Lady Genevieve:**
```
okay bestie so here's my UX take — users are gonna BOUNCE if we make them fill out a whole form before they see value 💀

here's what actually works:
1. let them explore FIRST (guest mode or demo)
2. THEN ask for signup when they're hooked
3. make signup stupid easy (Google OAuth >>> email/password)

also pls no "tell us about yourself" essays. nobody's got time for that. we can collect that data later through usage patterns fr fr

the vibe should be: "you're already in, just tell us your name real quick" not "fill out this application to maybe use our product" 🎨
```

### When You Use `!summon`

**You type:**
```
!summon Should we add social features to our app?
```

**Creates a Discord thread** where multiple courtiers debate:

```
🧵 Court Debate: Should we add social features to our app?

Lady Philippa (Coordinator):
okay so let's break this down bestie. social features could mean:
- user profiles
- following/followers
- comments/likes
- sharing
- DMs

what's the goal here Your Majesty? engagement? virality? network effects?

Lord Sebastian (Engineer):
real talk, social features are a MASSIVE scope increase. we're talking:
- user relationships database
- notification system
- moderation tools
- privacy controls
- scaling challenges

this is like 3-4 months of dev work minimum. are we ready for that? 🏗️

Lord Alistair (Strategy):
from a product perspective, social features are a double-edged sword...
[debate continues]
```

## 🎮 Commands Reference

| Command | What It Does | Who Can Use |
|---|---|---|
| `!court` | List all courtiers | Emperor only |
| `!status` | Check if bots are online | Emperor only |
| `!summon [topic]` | Start a court debate | Emperor only |
| `@[Courtier]` | Talk to specific courtier | Emperor only |

## 🔐 Security

Only YOU can command the court because `EMPEROR_USER_ID` is set to your Discord user ID (`1079667876115533855`).

If anyone else tries to use commands or @mention courtiers, they'll be ignored.

## 🎯 Next Steps After Deployment

1. Test each courtier individually
2. Try @mentioning multiple courtiers
3. Use `!summon` to start a debate
4. Start building your product with your court's help!

Your Gen Z royal dynasty is ready to serve! 👑
