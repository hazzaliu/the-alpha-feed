# 🚀 Ready to Deploy - The Emperor's Court

## ✅ Code is Ready!

All changes committed and pushed to GitHub. Railway will auto-deploy once you update the environment variables.

---

## 👑 Your Gender-Balanced Court (4 Ladies, 3 Lords)

### Ladies (She/Her):
1. **Lady Treasurer** - Finance queen, spreadsheet energy, "let's run the numbers bestie"
2. **Lady Envoy** - Marketing strategist, content creator vibes, "we're gonna make this blow up"
3. **Lady Vizier** - Coordinator, Notion girlie, "let's break this down bestie"
4. **Lady Jester** - UX advocate, brutally honest, "users gonna bounce fr"

### Lords (He/Him):
1. **Lord Architect** - Engineering genius, 3am coder, "that's a skill issue"
2. **Lord Herald** - News tracker, chronically online, "I called it"
3. **Lord Sage** - Strategy thinker, chess player energy, "what's the endgame?"

---

## 🎯 3 Steps to Deploy

### Step 1: Apply Supabase Schema ✅ (DO THIS FIRST)

1. Go to: https://supabase.com/dashboard/project/dezofblswtukueblxtli
2. Click **SQL Editor** in left sidebar
3. Copy this SQL and paste it:

```sql
-- Emperor's Court Database Schema

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

4. Click **Run**
5. Verify tables created: Go to Table Editor, you should see `conversations`, `courtier_responses`, `project_context`

---

### Step 2: Update Railway Variables ✅

1. Go to: https://railway.app
2. Open your project
3. Click on your service
4. Go to **Variables** tab
5. Click **Raw Editor**
6. Add this variable (your other variables should already be there):

```
EMPEROR_USER_ID=1079667876115533855
```

7. Click **Update Variables**
8. Railway will auto-redeploy from GitHub

**Your existing variables (should already be set):**
- `DISCORD_TOKEN` ✅
- `OPENAI_API_KEY` ✅
- `SUPABASE_URL` ✅
- `SUPABASE_KEY` ✅

---

### Step 3: Test in Discord ✅

Once Railway finishes deploying (watch the logs), test:

```
!status
```
Should show: "The Emperor's Court is assembled"

```
!court
```
Should list all 7 courtiers with Lord/Lady titles

```
@Lord Architect should I use React or Vue?
```
Should get a Gen Z response about tech stacks

```
@Lady Treasurer is $20/month good pricing?
```
Should get financial analysis

```
!summon Should we build mobile or web first?
```
Should create a debate thread with multiple courtiers

---

## 🎭 The Vibe

Each courtier has MAXIMUM Gen Z energy:

- **Lord Architect**: "bestie that's a skill issue", "we're so back", codes at 3am
- **Lady Treasurer**: "the math ain't mathing", That Girl energy, spreadsheet queen
- **Lord Herald**: "I called it", terminally online, Twitter-brain
- **Lady Envoy**: "this is giving viral", influencer energy, knows all platforms
- **Lady Vizier**: "let's break this down bestie", Notion girlie, organized chaos
- **Lord Sage**: "what's the endgame?", thinks 10 steps ahead, strategic AF
- **Lady Jester**: "users gonna bounce fr", brutally honest, will roast bad UX

---

## 💰 Cost: ~$15-45/month

- Railway: $5/month
- OpenAI: $10-30/month (depends on usage)
- Supabase: Free
- Tavily (optional web search): Free tier or $10/month

---

## ✅ Checklist:

- [x] Code written and tested
- [x] Committed to Git
- [x] Pushed to GitHub
- [ ] Supabase schema applied (DO THIS NOW)
- [ ] Railway variables updated with EMPEROR_USER_ID
- [ ] Test in Discord

---

Once you complete Steps 1 & 2, Railway will deploy automatically and your court will be ready to serve!

*The court awaits your command, Your Majesty* 👑
