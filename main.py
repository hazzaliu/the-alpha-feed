"""
The Emperor's Court — entry point.
Runs 7 separate Discord bots simultaneously, one for each courtier.
Each bot responds to @mentions and participates in debates.
"""

import os
import asyncio
import discord
from discord.ext import commands
from typing import Optional, Dict

from courtiers.lord_sebastian import LordSebastian
from courtiers.lady_beatrice import LadyBeatrice
from courtiers.lord_edmund import LordEdmund
from courtiers.lady_arabella import LadyArabella
from courtiers.lady_philippa import LadyPhilippa
from courtiers.lord_alistair import LordAlistair
from courtiers.lady_genevieve import LadyGenevieve
from services.debate_engine import DebateEngine
from services.context_manager import save_conversation, save_courtier_response
from services.web_search import web_search, format_search_results
from services.phase_coordinator import get_phase_coordinator, Phase, PhaseStatus

# Emperor's Discord user ID (only the Emperor can command the court)
EMPEROR_USER_ID = os.getenv("EMPEROR_USER_ID", "")

# Bot tokens for each courtier
LORD_SEBASTIAN_TOKEN = os.getenv("LORD_SEBASTIAN_TOKEN", "")
LADY_BEATRICE_TOKEN = os.getenv("LADY_BEATRICE_TOKEN", "")
LORD_EDMUND_TOKEN = os.getenv("LORD_EDMUND_TOKEN", "")
LADY_ARABELLA_TOKEN = os.getenv("LADY_ARABELLA_TOKEN", "")
LADY_PHILIPPA_TOKEN = os.getenv("LADY_PHILIPPA_TOKEN", "")
LORD_ALISTAIR_TOKEN = os.getenv("LORD_ALISTAIR_TOKEN", "")
LADY_GENEVIEVE_TOKEN = os.getenv("LADY_GENEVIEVE_TOKEN", "")

# Initialize all courtiers with their British royal names
courtiers = {
    "lord_sebastian": LordSebastian(),
    "lady_beatrice": LadyBeatrice(),
    "lord_edmund": LordEdmund(),
    "lady_arabella": LadyArabella(),
    "lady_philippa": LadyPhilippa(),
    "lord_alistair": LordAlistair(),
    "lady_genevieve": LadyGenevieve(),
}

# Map courtier keys to their tokens
courtier_tokens = {
    "lord_sebastian": LORD_SEBASTIAN_TOKEN,
    "lady_beatrice": LADY_BEATRICE_TOKEN,
    "lord_edmund": LORD_EDMUND_TOKEN,
    "lady_arabella": LADY_ARABELLA_TOKEN,
    "lady_philippa": LADY_PHILIPPA_TOKEN,
    "lord_alistair": LORD_ALISTAIR_TOKEN,
    "lady_genevieve": LADY_GENEVIEVE_TOKEN,
}

# Store bot instances
bots: Dict[str, commands.Bot] = {}

# Debate engines per channel (shared across all bots)
debate_engines = {}


def get_debate_engine(channel: discord.TextChannel) -> DebateEngine:
    """Get or create a debate engine for a channel."""
    if channel.id not in debate_engines:
        debate_engines[channel.id] = DebateEngine(channel)
    return debate_engines[channel.id]


def is_emperor(user: discord.User) -> bool:
    """Check if the user is the Emperor."""
    if not EMPEROR_USER_ID:
        return True  # If not configured, allow anyone (for testing)
    return str(user.id) == EMPEROR_USER_ID


def is_bot_mentioned(message: discord.Message, bot_user: discord.User) -> bool:
    """Check if this specific bot was @mentioned in the message."""
    # Check if bot was directly @mentioned
    if bot_user in message.mentions:
        return True
    return False


async def handle_philippa_coordination(reply_msg: discord.Message, response: str, original_msg: discord.Message):
    """
    Detect when Lady Philippa is coordinating a task and automatically:
    1. Create a thread
    2. Set up phase-based coordination
    3. @mention courtiers for Phase 1 only
    """
    # Detect coordination keywords
    coordination_keywords = ["PHASE 1:", "PHASE 2:", "COURTIER ASSIGNMENTS", "TASK BREAKDOWN"]
    is_coordinating = any(keyword in response for keyword in coordination_keywords)
    
    if not is_coordinating:
        return
    
    # Check if user said "proceed" in the original message
    user_approved = "proceed" in original_msg.content.lower()
    
    if not user_approved:
        # Philippa is just proposing a plan, not executing yet
        return
    
    # Parse phases from Philippa's response
    phases = parse_phases_from_response(response)
    
    if not phases:
        return
    
    # Create a thread
    try:
        thread = await reply_msg.create_thread(
            name=f"Task: {original_msg.content[:50]}...",
            auto_archive_duration=1440  # 24 hours
        )
        
        # Initialize phase coordinator
        phase_coordinator = get_phase_coordinator()
        task = phase_coordinator.create_task(
            thread=thread,
            task_name=original_msg.content[:100],
            phases=phases,
            emperor_user_id=str(original_msg.author.id)
        )
        
        # Start Phase 1
        task.current_phase.status = PhaseStatus.IN_PROGRESS
        
        # Find bot members in the guild
        guild = reply_msg.guild
        bot_members = {member.name: member for member in guild.members if member.bot}
        
        # Send phase overview
        await thread.send(
            f"📋 **PHASE-BASED COORDINATION ACTIVATED**\n\n"
            f"Your Majesty, I've broken this into {len(phases)} phases to keep things organized:\n\n" +
            "\n".join([f"{i+1}. {phase.name}" for i, phase in enumerate(phases)]) +
            f"\n\nStarting with **Phase 1: {phases[0].name}** fr fr 🎯"
        )
        
        # @mention courtiers for Phase 1 only
        phase_1 = phases[0]
        for courtier_key in phase_1.assigned_courtiers:
            # Convert courtier_key to display name
            courtier_display_name = courtier_key.replace("_", " ").title()
            
            # Find the matching bot member
            bot_member = None
            for name, member in bot_members.items():
                if courtier_display_name.lower() in name.lower():
                    bot_member = member
                    break
            
            if bot_member:
                await thread.send(
                    f"{bot_member.mention} **Phase 1 Task:** {phase_1.description}\n"
                    f"Deliverables: {', '.join(phase_1.deliverables)}"
                )
    
    except Exception as e:
        print(f"[Philippa Coordination] Error creating thread: {e}")


def parse_phases_from_response(response: str) -> List[Phase]:
    """Parse phase structure from Philippa's response."""
    phases = []
    lines = response.split("\n")
    
    current_phase = None
    courtier_map = {
        "sebastian": "lord_sebastian",
        "seb": "lord_sebastian",
        "beatrice": "lady_beatrice",
        "bea": "lady_beatrice",
        "edmund": "lord_edmund",
        "eddie": "lord_edmund",
        "arabella": "lady_arabella",
        "bella": "lady_arabella",
        "philippa": "lady_philippa",
        "pippa": "lady_philippa",
        "alistair": "lord_alistair",
        "ali": "lord_alistair",
        "genevieve": "lady_genevieve",
        "genny": "lady_genevieve",
    }
    
    for line in lines:
        # Detect phase headers
        if "PHASE 1:" in line or "Phase 1:" in line:
            if current_phase:
                phases.append(current_phase)
            current_phase = Phase(
                name=line.split(":", 1)[1].strip() if ":" in line else "Phase 1",
                description="",
                assigned_courtiers=[],
                deliverables=[]
            )
        elif "PHASE 2:" in line or "Phase 2:" in line:
            if current_phase:
                phases.append(current_phase)
            current_phase = Phase(
                name=line.split(":", 1)[1].strip() if ":" in line else "Phase 2",
                description="",
                assigned_courtiers=[],
                deliverables=[]
            )
        elif "PHASE 3:" in line or "Phase 3:" in line:
            if current_phase:
                phases.append(current_phase)
            current_phase = Phase(
                name=line.split(":", 1)[1].strip() if ":" in line else "Phase 3",
                description="",
                assigned_courtiers=[],
                deliverables=[]
            )
        elif current_phase:
            # Look for courtier names in the line
            line_lower = line.lower()
            for name, key in courtier_map.items():
                if name in line_lower and key not in current_phase.assigned_courtiers:
                    current_phase.assigned_courtiers.append(key)
            
            # Capture description
            if line.strip() and not line.strip().startswith("-"):
                current_phase.description += line.strip() + " "
    
    # Add last phase
    if current_phase and current_phase.assigned_courtiers:
        phases.append(current_phase)
    
    # If no phases detected, create a single phase with all courtiers
    if not phases:
        # Fallback: parse COURTIER ASSIGNMENTS section
        assignments = {}
        in_assignments = False
        
        for line in lines:
            if "COURTIER ASSIGNMENTS" in line:
                in_assignments = True
                continue
            if in_assignments and line.strip().startswith("-"):
                for name, key in courtier_map.items():
                    if name in line.lower() and key not in assignments:
                        assignments[key] = line.strip()
                        break
        
        if assignments:
            phases.append(Phase(
                name="Complete Task",
                description="All courtiers work together",
                assigned_courtiers=list(assignments.keys()),
                deliverables=["Complete deliverable"]
            ))
    
    return phases


def detect_courtier_mention(message: discord.Message) -> Optional[str]:
    """
    Detect which courtier was mentioned in the message.
    Returns courtier key or None.
    Supports both full names and nicknames.
    """
    content_lower = message.content.lower()
    
    # Check for @mentions by name/title/nickname
    if "sebastian" in content_lower or "seb" in content_lower or "architect" in content_lower:
        return "lord_sebastian"
    elif "beatrice" in content_lower or "bea" in content_lower or "treasurer" in content_lower:
        return "lady_beatrice"
    elif "edmund" in content_lower or "eddie" in content_lower or "herald" in content_lower:
        return "lord_edmund"
    elif "arabella" in content_lower or "bella" in content_lower or "envoy" in content_lower:
        return "lady_arabella"
    elif "philippa" in content_lower or "pippa" in content_lower or "vizier" in content_lower:
        return "lady_philippa"
    elif "alistair" in content_lower or "ali" in content_lower or "sage" in content_lower:
        return "lord_alistair"
    elif "genevieve" in content_lower or "genny" in content_lower or "jester" in content_lower:
        return "lady_genevieve"
    
    return None


async def handle_courtier_response(message: discord.Message, courtier_key: str, bot_instance: commands.Bot):
    """Handle a courtier responding to a message (from Emperor or another courtier)."""
    courtier = courtiers[courtier_key]
    
    # Determine who's speaking
    is_from_emperor = is_emperor(message.author)
    is_from_courtier = message.author.bot and not is_from_emperor
    
    # Extract the actual message (remove @mentions)
    clean_message = message.content
    for mention in message.mentions:
        clean_message = clean_message.replace(f"<@{mention.id}>", "")
    clean_message = clean_message.strip()
    
    if not clean_message:
        await message.reply(f"Your Majesty, what would you like me to do? 👀")
        return
    
    # Fetch conversation history (last 10 messages for context)
    conversation_history = []
    try:
        async for hist_msg in message.channel.history(limit=10, before=message):
            # Format: "Author: message content"
            author_name = hist_msg.author.name if hist_msg.author.name else "Unknown"
            msg_content = hist_msg.content[:200]  # Truncate long messages
            conversation_history.append(f"{author_name}: {msg_content}")
        
        # Reverse so oldest is first
        conversation_history.reverse()
    except Exception as e:
        print(f"[{courtier.name}] Could not fetch history: {e}")
    
    # Check for phase approval commands (Emperor only, in threads)
    if is_from_emperor and isinstance(message.channel, discord.Thread):
        approval_keywords = ["approve", "approved", "next phase", "move to next", "proceed to next"]
        if any(keyword in clean_message.lower() for keyword in approval_keywords):
            phase_coordinator = get_phase_coordinator()
            task = phase_coordinator.get_task(message.channel.id)
            if task and task.current_phase and task.current_phase.status == PhaseStatus.COMPLETED:
                # Approve current phase and move to next
                phase_coordinator.approve_phase(message.channel.id)
                
                if task.is_complete:
                    await message.reply(
                        f"🎉 Your Majesty, all phases are complete! "
                        f"The task is done fr fr. Lady Philippa will present the final deliverable!"
                    )
                    phase_coordinator.cleanup_task(message.channel.id)
                    return
                else:
                    # Start next phase
                    next_phase = task.current_phase
                    await message.reply(
                        f"✅ Phase approved! Moving to **{next_phase.name}**\n\n"
                        f"Summoning courtiers for this phase..."
                    )
                    
                    # @mention courtiers for next phase
                    guild = message.guild
                    bot_members = {member.name: member for member in guild.members if member.bot}
                    
                    for courtier_key in next_phase.assigned_courtiers:
                        courtier_display_name = courtier_key.replace("_", " ").title()
                        bot_member = None
                        for name, member in bot_members.items():
                            if courtier_display_name.lower() in name.lower():
                                bot_member = member
                                break
                        
                        if bot_member:
                            await message.channel.send(
                                f"{bot_member.mention} **{next_phase.name} Task:** {next_phase.description}\n"
                                f"Deliverables: {', '.join(next_phase.deliverables) if next_phase.deliverables else 'Complete your assigned work'}"
                            )
                    return
    
    # Build context based on who's speaking
    context = {}
    if is_from_courtier:
        # Another courtier is speaking - this is a collaboration
        sender_name = message.author.name
        context["speaker"] = sender_name
        context["conversation_type"] = "courtier_collaboration"
        clean_message = f"[{sender_name} is asking you]: {clean_message}"
    
    # Add conversation history to context
    if conversation_history:
        context["conversation_history"] = "\n".join(conversation_history)
    
    # Add phase context if in a coordinated task
    if isinstance(message.channel, discord.Thread):
        phase_coordinator = get_phase_coordinator()
        task = phase_coordinator.get_task(message.channel.id)
        if task and task.current_phase:
            context["current_phase"] = task.current_phase.name
            context["phase_status"] = task.current_phase.status.value
    
    
    # Show typing indicator
    async with message.channel.typing():
        try:
            # Special handling for courtiers with web search
            if courtier_key in ["lord_edmund", "lady_arabella"] and hasattr(courtier, "has_web_search"):
                # Determine if we should search
                search_triggers = ["what's", "whats", "trending", "happening", "latest", "news", 
                                 "competitor", "doing", "is ", "are ", "how are", "search"]
                should_search = any(trigger in clean_message.lower() for trigger in search_triggers)
                
                if should_search:
                    # Perform web search
                    search_results = await web_search(clean_message, max_results=5)
                    search_context = format_search_results(search_results)
                    
                    # Add search results to context
                    context["web_search_results"] = search_context
                    context["search_query"] = clean_message
                    response = await courtier.respond(
                        f"Based on current web search results, {clean_message}",
                        context
                    )
                else:
                    response = await courtier.respond(clean_message, context)
            else:
                response = await courtier.respond(clean_message, context)
            
            # Send response (no title prefix since bot username already shows it)
            reply_msg = await message.reply(response)
            
            # Record response in phase coordinator (if in a thread with active task)
            if isinstance(message.channel, discord.Thread):
                phase_coordinator = get_phase_coordinator()
                phase_coordinator.record_response(message.channel.id, courtier_key, response)
                
                # Check if phase is complete
                if phase_coordinator.is_phase_complete(message.channel.id):
                    # Notify Philippa to synthesize
                    task = phase_coordinator.get_task(message.channel.id)
                    if task and task.current_phase:
                        # Find Philippa bot
                        philippa_bot = None
                        for member in message.guild.members:
                            if member.bot and "philippa" in member.name.lower():
                                philippa_bot = member
                                break
                        
                        if philippa_bot:
                            await message.channel.send(
                                f"{philippa_bot.mention} all courtiers in **{task.current_phase.name}** "
                                f"have responded! Please synthesize their work fr fr 📋"
                            )
            
            # Special handling for Lady Philippa's coordination
            if courtier_key == "lady_philippa" and is_from_emperor:
                await handle_philippa_coordination(reply_msg, response, message)
            
            # Save to database
            try:
                conv_id = await save_conversation(
                    emperor_message_id=str(message.id),
                    context={"original_message": clean_message}
                )
                await save_courtier_response(
                    conversation_id=conv_id,
                    courtier_name=courtier.name,
                    response_text=response
                )
            except Exception as db_error:
                print(f"[{courtier.name}] Database save error: {db_error}")
        
        except Exception as e:
            await message.reply(
                f"💀 bestie something's cooked on my end\n"
                f"```{str(e)[:200]}```\n"
                f"*gonna need Lord Sebastian to debug this fr fr*"
            )
            print(f"[{courtier.name}] Error: {e}")


def create_bot_for_courtier(courtier_key: str) -> commands.Bot:
    """Create a Discord bot instance for a specific courtier."""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    courtier = courtiers[courtier_key]
    
    @bot.event
    async def on_ready():
        print(f"✓ [{courtier.name}] Online and ready to serve His Imperial Majesty")
        print(f"  └─ Username: {bot.user.name}")
        print(f"  └─ ID: {bot.user.id}")
        if EMPEROR_USER_ID:
            print(f"  └─ Serving Emperor ID: {EMPEROR_USER_ID}")
        print()
    
    @bot.event
    async def on_message(message: discord.Message):
        """Listen for @mentions of this courtier."""
        # Ignore own messages
        if message.author == bot.user:
            return
        
        # In threads: Check phase-based coordination
        if isinstance(message.channel, discord.Thread):
            # Check if this bot was @mentioned (by Emperor OR another bot)
            if is_bot_mentioned(message, bot.user):
                # Check if courtier is allowed to respond in current phase
                phase_coordinator = get_phase_coordinator()
                if phase_coordinator.is_courtier_allowed_to_respond(message.channel.id, courtier_key):
                    await handle_courtier_response(message, courtier_key, bot)
                else:
                    # Courtier not in current phase
                    await message.reply(
                        f"Your Majesty, I'm not assigned to this phase rn! "
                        f"Lady Philippa will summon me when it's my turn fr fr 👀"
                    )
        else:
            # In main channels: Only respond to Emperor
            if message.author.bot:
                return
            
            if not is_emperor(message.author):
                return
            
            # Check if this bot was @mentioned
            if is_bot_mentioned(message, bot.user):
                await handle_courtier_response(message, courtier_key, bot)
        
        # Process commands
        await bot.process_commands(message)
    
    @bot.command(name="court")
    async def court_command(ctx: commands.Context):
        """!court — list all courtiers."""
        if not is_emperor(ctx.author):
            return
        
        court_list = "👑 **THE EMPEROR'S COURT** 👑\n\n"
        court_list += "Your Majesty, here are your courtiers:\n\n"
        
        for c in courtiers.values():
            pronoun_emoji = "👨" if c.pronouns == "he/him" else "👩"
            court_list += f"{pronoun_emoji} **{c.title}**\n"
            court_list += f"   └─ {c.role}\n"
            if hasattr(c, 'nickname'):
                court_list += f"   └─ Nickname: {c.nickname}\n"
            court_list += "\n"
        
        court_list += "*To speak with a courtier, @mention them in your message*\n"
        court_list += "Example: `@Lord Sebastian help me with this code`"
        
        await ctx.send(court_list)
    
    @bot.command(name="status")
    async def status_command(ctx: commands.Context):
        """!status — check if this courtier is online."""
        await ctx.send(
            f"✅ **{courtier.title}** reporting for duty, Your Majesty! 🙇\n\n"
            f"*I'm ready to assist with {courtier.role.lower()}*\n"
            f"Mention me anytime you need help!"
        )
    
    return bot


async def run_all_bots():
    """Run all 7 courtier bots simultaneously."""
    print("[main] Checking environment variables...")
    
    # Validate all tokens are present
    missing_tokens = []
    for courtier_key, token in courtier_tokens.items():
        if not token:
            missing_tokens.append(courtier_key)
            print(f"[ERROR] Missing token for {courtier_key}")
    
    if missing_tokens:
        print(f"\n[FATAL] Cannot start. Missing {len(missing_tokens)} tokens:")
        for key in missing_tokens:
            print(f"  - {key.upper()}_TOKEN")
        print("\nAdd these to Railway → Variables tab")
        return
    
    print(f"[main] All {len(courtier_tokens)} tokens found ✓")
    print(f"[main] Starting {len(courtier_tokens)} courtier bots...")
    print(f"[main] The Emperor's Court is assembling...\n")
    
    tasks = []
    
    for courtier_key, token in courtier_tokens.items():
        bot_instance = create_bot_for_courtier(courtier_key)
        bots[courtier_key] = bot_instance
        
        # Create task to run this bot
        task = asyncio.create_task(bot_instance.start(token))
        tasks.append(task)
    
    # Run all bots concurrently
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"\n[FATAL] Error running bots: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        print("[main] The Emperor's Court has been dismissed.")
