# 🧠 How Courtiers Understand Context

## The Problem (SOLVED ✅)

Before: When you said "the above" or "what we just discussed", courtiers had no idea what you were talking about.

**Now: Courtiers can read the conversation history!**

---

## How It Works

When you @mention a courtier, they automatically receive:
1. **Your current message**
2. **The last 10 messages** in the channel/thread (conversation history)

They can see:
- What you said earlier
- What other courtiers said
- The full context of the discussion

---

## Examples

### Example 1: "The Above"

**You:**
```
@Lady Philippa, Grand Vizier can you help coordinate a plan from the team for me to assess the feasibility of building a financial tracker?
```

**Philippa responds with a plan**

**You:**
```
@Lady Philippa, Grand Vizier what's the status of the above
```

**Philippa now sees:**
- Her previous message (the plan she created)
- Your original request (the financial tracker)
- She understands "the above" = the financial tracker plan

---

### Example 2: "That"

**Thread conversation:**
```
@Lord Sebastian, Grand Architect: "Your Majesty, we should use React + FastAPI for this"
@Lady Beatrice, Royal Treasurer: "Your Majesty, that stack costs $50/mo to host"
```

**You:**
```
@Lord Alistair, Royal Sage what do you think about that
```

**Alistair sees:**
- Sebastian's tech stack recommendation
- Beatrice's cost analysis
- He understands "that" = the React + FastAPI stack decision

---

### Example 3: "Synthesize This"

**Thread with multiple courtiers responding:**
```
@Lord Sebastian: [technical architecture]
@Lady Genevieve: [UX design]
@Lady Beatrice: [cost analysis]
@Lord Edmund: [market research]
```

**You:**
```
@Lady Philippa, Grand Vizier synthesize this
```

**Philippa sees:**
- All 4 courtiers' responses
- The full discussion
- She can create a comprehensive final report

---

## What Courtiers Can See

### In Conversation History:
- ✅ Previous messages from you (His Majesty)
- ✅ Previous messages from other courtiers
- ✅ The order of messages (who said what when)
- ✅ Up to the last 10 messages

### What They DON'T See:
- ❌ Messages from other channels (only the current channel/thread)
- ❌ Messages older than the last 10 (for performance)
- ❌ Deleted messages
- ❌ Messages from before the bot was added to the server

---

## Best Practices

### ✅ DO:
- Say "the above" or "that" — courtiers will understand
- Reference previous messages naturally
- Ask courtiers to build on each other's work
- Use "synthesize this" to have Philippa summarize discussions

### ❌ DON'T:
- Reference things from other channels (they can't see those)
- Reference things from days ago (only last 10 messages are visible)
- Assume they remember things from previous sessions (each @mention is fresh)

---

## Pro Tips

### 1. Use Threads for Complex Tasks
When coordinating multiple courtiers, create a thread. This keeps all the context in one place:
```
1. @Lady Philippa creates plan
2. You @mention courtiers in thread
3. Courtiers discuss and respond
4. @Lady Philippa synthesizes (she sees everything in the thread)
```

### 2. Reference Courtiers by Name
Instead of:
```
@Lady Philippa what do you think about the tech stack
```

Be more specific if needed:
```
@Lady Philippa what do you think about Sebastian's tech stack recommendation
```

Though now she can see Sebastian's message in the history!

### 3. Ask for Synthesis
After courtiers discuss, ask Philippa to synthesize:
```
@Lady Philippa, Grand Vizier synthesize what everyone said
```

She'll read all the messages and create a final report.

---

## Technical Details (For Nerds)

- **History Limit:** Last 10 messages (configurable in `main.py`)
- **Format:** `Author: message content` (truncated to 200 chars per message)
- **Passed to LLM:** Wrapped in `[RECENT CONVERSATION ABOVE]` markers
- **Performance:** Minimal overhead (~100ms to fetch history)

---

## Try It Now!

Go back to Discord and try:

1. @mention a courtier with a question
2. Then @mention another courtier saying "what do you think about that"
3. They'll understand the context! 🎯

---

**Your courtiers are now context-aware! 🧠👑**
