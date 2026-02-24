# 🚀 The Emperor's Court - Complete Setup Instructions

## 👑 Your British Royal Gen Z Court

**4 Ladies:** Beatrice, Arabella, Philippa, Genevieve
**3 Lords:** Sebastian, Edmund, Alistair

Each with full Gen Z energy and distinct personalities!

---

## 📋 Complete Setup Checklist

### ✅ Phase 1: Create 7 Discord Bots (~20-30 minutes)

Follow the guide in `CREATE_7_BOTS_GUIDE.md` to create each bot.

**Quick version:**
1. Go to https://discord.com/developers/applications
2. Create 7 applications with these EXACT names:
   - `Lord Sebastian, Grand Architect`
   - `Lady Beatrice, Royal Treasurer`
   - `Lord Edmund, Court Herald`
   - `Lady Arabella, Royal Envoy`
   - `Lady Philippa, Grand Vizier`
   - `Lord Alistair, Royal Sage`
   - `Lady Genevieve, Court Jester`
3. For each: Enable bot, enable 3 intents, copy token, invite to server
4. Save all 7 tokens

---

### ✅ Phase 2: Apply Supabase Schema (~2 minutes)

1. Go to: https://supabase.com/dashboard/project/dezofblswtukueblxtli
2. Click **SQL Editor**
3. Copy and run this SQL:

```sql
create table if not exists conversations (
    id bigserial primary key,
    emperor_message_id text not null,
    thread_id text,
    context jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_conversations_created_at on conversations(created_at desc);
create index if not exists idx_conversations_thread_id on conversations(thread_id);

create table if not exists courtier_responses (
    id bigserial primary key,
    conversation_id bigint references conversations(id) on delete cascade,
    courtier_name text not null,
    response_text text,
    response_json jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_courtier_responses_conversation on courtier_responses(conversation_id);
create index if not exists idx_courtier_responses_courtier on courtier_responses(courtier_name);
create index if not exists idx_courtier_responses_created_at on courtier_responses(created_at desc);

create table if not exists project_context (
    id bigserial primary key,
    project_name text not null unique,
    description text,
    tech_stack jsonb,
    decisions jsonb,
    updated_at timestamptz not null default now()
);

create index if not exists idx_project_context_updated_at on project_context(updated_at desc);
```

4. Verify tables created: Go to **Table Editor**, should see `conversations`, `courtier_responses`, `project_context`

---

### ✅ Phase 3: Update Code for 7 Bots (~5 minutes - I'll do this)

Once you give me all 7 tokens, I'll update the code to:
- Run all 7 Discord bot clients simultaneously
- Each bot responds only to their own @mentions
- All can participate in debates together
- Single Railway deployment running all 7

---

### ✅ Phase 4: Deploy to Railway (~5 minutes)

1. Go to: https://railway.app
2. Open your project
3. Go to **Variables** tab
4. Add all environment variables:

```
DISCORD_TOKEN=<remove this old single token>
LORD_SEBASTIAN_TOKEN=your_token_here
LADY_BEATRICE_TOKEN=your_token_here
LORD_EDMUND_TOKEN=your_token_here
LADY_ARABELLA_TOKEN=your_token_here
LADY_PHILIPPA_TOKEN=your_token_here
LORD_ALISTAIR_TOKEN=your_token_here
LADY_GENEVIEVE_TOKEN=your_token_here
OPENAI_API_KEY=<already set>
SUPABASE_URL=<already set>
SUPABASE_KEY=<already set>
EMPEROR_USER_ID=1079667876115533855
```

5. Railway auto-deploys from GitHub

---

### ✅ Phase 5: Test in Discord (~5 minutes)

Once deployed, test each courtier:

```
@Lord Sebastian should I use React or Vue?
@Lady Beatrice is $20/month good pricing?
@Lord Edmund what's trending in AI?
@Lady Arabella how do we launch this?
@Lady Philippa I want to build a todo app
@Lord Alistair should we add social features?
@Lady Genevieve is this UI too complex?
```

Test debate mode:
```
!summon Should we build mobile or web first?
```

---

## 🎭 How They'll Respond

**Lord Sebastian (Seb):** "bestie that's a skill issue, here's the fix fr fr 💻"

**Lady Beatrice (Bea):** "okay let's run the numbers on this bestie 📊"

**Lord Edmund (Eddie):** "yo I was just on Twitter and this is trending rn 📰"

**Lady Arabella (Bella):** "we're gonna make this blow up, here's the strategy 🚀"

**Lady Philippa (Pippa):** "let's break this down bestie, clarifying question: 📋"

**Lord Alistair (Ali):** "okay but what's the endgame? zoom out for a sec 🎯"

**Lady Genevieve (Genny):** "users gonna bounce fr, this UI is giving confusing 💀"

---

## 📊 Current Status

✅ Code updated with British royal names
✅ All imports tested and working
✅ Committed and pushed to GitHub
⏳ Waiting for you to create 7 Discord bots
⏳ Waiting for Supabase schema to be applied
⏳ Then I'll update code for 7-bot deployment

---

## 🎯 Your Next Steps

1. **Create the 7 Discord bots** (use `CREATE_7_BOTS_GUIDE.md`)
2. **Apply Supabase SQL** (copy SQL from above)
3. **Send me all 7 tokens** (I'll update the code)
4. **I'll push to GitHub**
5. **You update Railway variables**
6. **Test in Discord!**

---

**Total time: ~40 minutes from start to finish**

Let me know when you have the 7 bot tokens ready! 👑
