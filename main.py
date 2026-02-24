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
    
    # Build context based on who's speaking
    context = {}
    if is_from_courtier:
        # Another courtier is speaking - this is a collaboration
        sender_name = message.author.name
        context["speaker"] = sender_name
        context["conversation_type"] = "courtier_collaboration"
        clean_message = f"[{sender_name} is asking you]: {clean_message}"
    
    # Show typing indicator
    async with message.channel.typing():
        try:
            # Special handling for courtiers with web search
            if courtier_key in ["lord_edmund", "lady_arabella"] and hasattr(courtier, "has_web_search"):
                # Determine if we should search
                search_triggers = ["what's", "whats", "trending", "happening", "latest", "news", 
                                 "competitor", "doing", "is ", "are ", "how are", "search"]
                should_search = any(trigger in emperor_message.lower() for trigger in search_triggers)
                
                if should_search:
                    # Perform web search
                    search_results = await web_search(emperor_message, max_results=5)
                    search_context = format_search_results(search_results)
                    
                    # Add search results to context
                    context = {
                        "web_search_results": search_context,
                        "search_query": emperor_message
                    }
                    response = await courtier.respond(
                        f"Based on current web search results, {emperor_message}",
                        context
                    )
                else:
                    response = await courtier.respond(emperor_message)
            else:
                response = await courtier.respond(emperor_message)
            
            # Send response (no title prefix since bot username already shows it)
            await message.reply(response)
            
            # Save to database
            try:
                conv_id = await save_conversation(
                    emperor_message_id=str(message.id),
                    context={"original_message": emperor_message}
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
        
        # In threads: Allow bots to talk to each other
        if isinstance(message.channel, discord.Thread):
            # Check if this bot was @mentioned (by Emperor OR another bot)
            if is_bot_mentioned(message, bot.user):
                await handle_courtier_response(message, courtier_key, bot)
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
