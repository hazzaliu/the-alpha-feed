# 👑 How to Coordinate Your Court

## The Workflow You Want

You (the King) → Lady Philippa (coordinates) → Other courtiers (execute) → Philippa (reports back)

## How It Works

### Option 1: Direct Coordination (Simplest)

**You:** Give Lady Philippa a task and she'll coordinate

```
@Lady Philippa build me a landing page for my productivity app
```

**Philippa:** Creates a plan and asks for approval

```
Your Majesty, okay bet let me coordinate this 📋

TASK BREAKDOWN:
- UX design & layout → @Lady Genevieve
- Technical build → @Lord Sebastian  
- Marketing copy → @Lady Arabella
- Final synthesis → me

PLAN:
1. Genny designs the user flow
2. Seb codes it up
3. Bella writes compelling copy
4. I put it all together and deliver

Does this work Your Majesty? Reply 'proceed' and I'll get the court working fr fr 🎯
```

**You:** Approve

```
proceed
```

**Philippa:** Coordinates in a thread

She'll @mention the other courtiers in the thread, they'll each do their part, then she synthesizes everything into a final report for you.

### Option 2: Use the !summon Command

**You:** Start a court discussion

```
!summon Should we add social features to our app?
```

**Result:** Creates a thread where multiple courtiers debate, then Philippa synthesizes the consensus.

### Option 3: Direct Multi-Mention

**You:** @mention multiple courtiers at once

```
@Lord Sebastian @Lady Genevieve how should we design the onboarding flow?
```

**Result:** Both bots respond with their perspectives (Sebastian: technical, Genevieve: UX)

## Best Practices

### For Building Things (Coordination)

Use Lady Philippa as your coordinator:

```
@Lady Philippa I need to:
- Build a landing page
- Create a pricing strategy
- Launch on Product Hunt
- Optimize our signup flow
- Design a new feature
```

She'll:
1. Break it down
2. Assign courtiers
3. Coordinate their work
4. Report back with deliverables

### For Decisions (Debates)

Use !summon for strategic decisions:

```
!summon Should we pivot to B2B?
!summon Which tech stack should we use?
!summon Is this feature worth building?
```

Multiple courtiers will debate, Philippa synthesizes.

### For Quick Questions (Direct)

@mention the specific courtier:

```
@Lord Sebastian what's the best database?
@Lady Beatrice is $29/month good pricing?
@Lord Edmund what's trending in AI?
```

They respond directly, no coordination needed.

## Example Full Workflow

### Scenario: You want to build a new feature

**Step 1: You give the high-level task**
```
@Lady Philippa I want to add user authentication to my app
```

**Step 2: Philippa breaks it down**
```
Your Majesty, okay bet authentication is a big one. Let me coordinate the court 📋

TASK BREAKDOWN:
- Technical architecture → @Lord Sebastian
- UX flow (signup/login) → @Lady Genevieve
- Security & cost → @Lady Beatrice
- Strategic fit → @Lord Alistair

PLAN:
1. Ali confirms this aligns with product vision
2. Seb designs the auth architecture
3. Genny designs the signup/login UX
4. Bea reviews costs (auth providers, security)
5. I synthesize into an implementation plan

Does this work Your Majesty? Say 'proceed' and I'll assemble the court fr fr 🎯
```

**Step 3: You approve**
```
proceed
```

**Step 4: Philippa coordinates (creates thread)**

Thread: "Task: Add user authentication"

```
@Lord Alistair @Lord Sebastian @Lady Genevieve @Lady Beatrice

Your Majesty wants to add user authentication. Here's what I need from each of you:

@Lord Alistair - Does auth fit our product strategy? Should we do it now or later?

@Lord Sebastian - Technical architecture: email/password vs OAuth? Database schema? Security best practices?

@Lady Genevieve - UX flow: How many steps? What info do we collect? Mobile-friendly?

@Lady Beatrice - Cost analysis: Auth0 vs Supabase Auth vs custom? What's the monthly cost?

Let's go courtiers, His Majesty is waiting 👑
```

**Step 5: Each courtier responds in the thread**

**Lord Alistair:**
> "Your Majesty, strategically this makes sense if we're going multi-user. Auth is table stakes for SaaS. The move is to do it now before we have too many users to migrate. Slay decision fr 🎯"

**Lord Sebastian:**
> "yo Your Majesty, okay so for auth I'm thinking Supabase Auth lowkey goes hard. It's built-in, secure, handles OAuth, and we're already using Supabase. Email/password + Google OAuth is the move. I can have this shipped in like 3 days no cap 💻"

**Lady Genevieve:**
> "okay Your Majesty, for UX keep it SIMPLE. 2-step signup: email + password, verify email, done. Add Google OAuth button for the lazy users (most people). Login should be one page, no complicated flows. Users gonna bounce if signup takes more than 2 mins fr fr ✨"

**Lady Beatrice:**
> "Your Majesty, okay so Supabase Auth is free tier up to 50k users, then $0.00325 per MAU after that. Way cheaper than Auth0 ($240/mo minimum). If Seb says Supabase works technically, that's the financially smart move. Your Majesty ate with this timing btw, better to add auth now than migrate later 💰"

**Step 6: Philippa synthesizes and reports**

```
═══════════════════════════════════════
📋 FINAL REPORT TO HIS MAJESTY 📋
═══════════════════════════════════════

Your Majesty, the court has deliberated on user authentication!

SUMMARY:
The court unanimously recommends implementing authentication NOW using Supabase Auth.

KEY DELIVERABLES:
✅ Strategic Alignment (Ali): Auth is essential for multi-user SaaS, do it before scaling
✅ Technical Plan (Seb): Supabase Auth with email/password + Google OAuth, 3-day implementation
✅ UX Design (Genny): 2-step signup, one-page login, mobile-optimized
✅ Cost Analysis (Bea): Free up to 50k users, then $0.00325/user - most cost-effective option

RECOMMENDATIONS:
1. Use Supabase Auth (already integrated, secure, cheap)
2. Implement email/password + Google OAuth
3. Keep signup to 2 steps maximum
4. Timeline: 3 days for Lord Sebastian to build
5. Budget: $0 initially, scales affordably

NEXT STEPS:
- Approve this plan
- Lord Sebastian will build it
- Lady Genevieve will review UX before launch
- I'll track progress and keep you updated

STATUS: Ready to execute, Your Majesty. Say the word and Seb will start coding fr fr 🚀

*The court has served. Awaiting your command* 🙇
```

**Step 7: You decide**
```
looks good, proceed
```

**Step 8: Philippa coordinates execution**

She'll keep you updated as Sebastian builds, Genevieve reviews, etc. When it's done, she reports back with the final deliverable.

## Commands Reference

| What You Want | Command | What Happens |
|---|---|---|
| **Build something** | `@Lady Philippa build X` | She coordinates courtiers, reports back |
| **Make a decision** | `!summon Should we do X?` | Courtiers debate, Philippa synthesizes |
| **Quick question** | `@[Specific Courtier] question` | That courtier responds directly |
| **See all courtiers** | `!court` | Lists all 7 courtiers |
| **Check status** | `!status` | Bot confirms it's online |

## Pro Tips

### Delegate to Philippa

Instead of managing each courtier yourself, give Philippa the task:

**Don't do this:**
```
@Lord Sebastian build the backend
@Lady Genevieve design the UI
@Lady Arabella write the copy
```
(You're micromanaging)

**Do this:**
```
@Lady Philippa I need a landing page built
```
(She coordinates everything and reports back)

### Let Philippa Handle Complexity

For complex multi-step tasks:
- Give Philippa the high-level goal
- She breaks it down
- She assigns courtiers
- She tracks progress
- She reports back when done

You just lead, she executes.

### Use Direct @mentions for Simple Stuff

For quick questions, skip Philippa:
```
@Lord Sebastian is React good for this?
@Lady Beatrice what should I charge?
```

No coordination needed for simple questions.

## The Dynamic

Think of it like this:

**You (King):**
- Set the vision
- Make final decisions
- Give high-level tasks

**Lady Philippa (Grand Vizier):**
- Breaks down your tasks
- Coordinates the other 6 courtiers
- Synthesizes their work
- Reports back to you
- Your right hand

**Other 6 Courtiers:**
- Execute their domain expertise
- Report to Philippa
- Philippa delivers to you

It's like having a Chief of Staff who manages your team for you!

---

## Try It Now

Once Railway finishes deploying, try:

```
@Lady Philippa I want to build a pricing page for my SaaS
```

She'll create a plan, coordinate Sebastian (code), Genevieve (UX), Beatrice (pricing strategy), Arabella (copy), and report back with everything done!

You just lead. Philippa coordinates. The court executes. 👑
