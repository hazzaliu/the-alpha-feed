"""
The Emperor's Court — entry point.
Routes @mentions to courtiers, coordinates debates, serves His Imperial Majesty.
"""

import os
import discord
from discord.ext import commands
from typing import Optional

from courtiers.lord_architect import LordArchitect
from courtiers.lady_treasurer import LadyTreasurer
from courtiers.lord_herald import LordHerald
from courtiers.lady_envoy import LadyEnvoy
from courtiers.lady_vizier import LadyVizier
from courtiers.lord_sage import LordSage
from courtiers.lady_jester import LadyJester
from services.debate_engine import DebateEngine
from services.context_manager import save_conversation, save_courtier_response
from services.web_search import web_search, format_search_results

from config import DISCORD_TOKEN

# Emperor's Discord user ID (only the Emperor can command the court)
EMPEROR_USER_ID = os.getenv("EMPEROR_USER_ID", "")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize all courtiers
courtiers = {
    "lord_architect": LordArchitect(),
    "lady_treasurer": LadyTreasurer(),
    "lord_herald": LordHerald(),
    "lady_envoy": LadyEnvoy(),
    "lady_vizier": LadyVizier(),
    "lord_sage": LordSage(),
    "lady_jester": LadyJester(),
}

# Debate engines per channel
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


def detect_courtier_mention(message: discord.Message) -> Optional[str]:
    """
    Detect which courtier was mentioned in the message.
    Returns courtier key or None.
    """
    content_lower = message.content.lower()
    
    # Check for @mentions by name/title
    if "lord architect" in content_lower or "@lord architect" in content_lower or "architect" in content_lower:
        return "lord_architect"
    elif "lady treasurer" in content_lower or "@lady treasurer" in content_lower or "treasurer" in content_lower:
        return "lady_treasurer"
    elif "lord herald" in content_lower or "@lord herald" in content_lower or "herald" in content_lower:
        return "lord_herald"
    elif "lady envoy" in content_lower or "@lady envoy" in content_lower or "envoy" in content_lower:
        return "lady_envoy"
    elif "lady vizier" in content_lower or "@lady vizier" in content_lower or "vizier" in content_lower:
        return "lady_vizier"
    elif "lord sage" in content_lower or "@lord sage" in content_lower or "sage" in content_lower:
        return "lord_sage"
    elif "lady jester" in content_lower or "@lady jester" in content_lower or "jester" in content_lower:
        return "lady_jester"
    
    return None


async def handle_courtier_response(message: discord.Message, courtier_key: str):
    """Handle a courtier responding to the Emperor's message."""
    courtier = courtiers[courtier_key]
    
    # Extract the Emperor's actual message (remove the mention)
    emperor_message = message.content
    for name in ["lord architect", "lady treasurer", "lord herald", "lady envoy", 
                 "lady vizier", "lord sage", "lady jester"]:
        emperor_message = emperor_message.replace(f"@{name}", "").replace(name, "")
    emperor_message = emperor_message.strip()
    
    if not emperor_message:
        await message.reply(f"Your Majesty, what would you like me to do? 👀")
        return
    
    # Show typing indicator
    async with message.channel.typing():
        try:
            # Special handling for courtiers with web search
            if courtier_key in ["lord_herald", "lady_envoy"] and hasattr(courtier, "has_web_search"):
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
            
            # Send response with courtier title
            await message.reply(f"**{courtier.title}**: {response}")
            
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
                print(f"[main] Database save error: {db_error}")
        
        except Exception as e:
            await message.reply(
                f"💀 **{courtier.title}**: bestie something's cooked on my end\n"
                f"```{str(e)[:200]}```\n"
                f"*gonna need the Grand Architect to debug this fr fr*"
            )
            print(f"[main] Courtier error ({courtier_key}): {e}")


@bot.event
async def on_ready():
    print(f"[main] The Emperor's Court is assembled. Serving {bot.user}")
    print(f"[main] Courtiers ready: {', '.join([c.name for c in courtiers.values()])}")
    if EMPEROR_USER_ID:
        print(f"[main] Serving Emperor ID: {EMPEROR_USER_ID}")
    else:
        print("[main] WARNING: EMPEROR_USER_ID not set. All users can command the court.")


@bot.event
async def on_message(message: discord.Message):
    """Listen for @mentions of courtiers."""
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check if Emperor
    if not is_emperor(message.author):
        # Only respond to non-Emperor in threads (debate mode)
        if isinstance(message.channel, discord.Thread):
            pass  # Allow in threads for debates
        else:
            return  # Ignore non-Emperor in main channels
    
    # Detect courtier mention
    courtier_key = detect_courtier_mention(message)
    
    if courtier_key:
        # Single courtier mentioned
        await handle_courtier_response(message, courtier_key)
    
    # Process commands
    await bot.process_commands(message)


@bot.command(name="court")
async def court_command(ctx: commands.Context):
    """!court — list all courtiers and their roles."""
    if not is_emperor(ctx.author):
        return
    
    court_list = "👑 **THE EMPEROR'S COURT** 👑\n\n"
    court_list += "Your Majesty, here are your courtiers:\n\n"
    
    for courtier in courtiers.values():
        court_list += f"**{courtier.title}**\n"
        court_list += f"└─ {courtier.role}\n"
        court_list += f"└─ Mention: `@{courtier.name}`\n\n"
    
    court_list += "\n*To summon a courtier, mention them in your message*\n"
    court_list += "Example: `@Grand Architect help me with this code`"
    
    await ctx.send(court_list)


@bot.command(name="summon")
async def summon_command(ctx: commands.Context, *, topic: str = ""):
    """!summon [topic] — Start a court debate with multiple courtiers."""
    if not is_emperor(ctx.author):
        return
    
    if not topic:
        await ctx.send("Your Majesty, what shall the court discuss? Usage: `!summon [topic]`")
        return
    
    # By default, summon key courtiers for product building
    debate_courtiers = [
        courtiers["lady_vizier"],  # Coordinates
        courtiers["lord_architect"],  # Technical
        courtiers["lord_sage"],  # Strategy
        courtiers["lady_jester"],  # UX
    ]
    
    debate_engine = get_debate_engine(ctx.channel)
    thread = await debate_engine.start_debate(
        initial_message=ctx.message,
        courtiers=debate_courtiers,
        topic=topic
    )
    
    await ctx.send(f"👥 The court has been summoned to debate: **{topic}**\n"
                   f"The discussion continues in {thread.mention}")


@bot.command(name="status")
async def status_command(ctx: commands.Context):
    """!status — check if the court is assembled."""
    await ctx.send(
        "✅ **The Emperor's Court is assembled** 👑\n\n"
        f"**Active Courtiers**: {len(courtiers)}\n"
        f"**Use `!court`** to see all courtiers\n"
        f"**Use `@[Courtier Name]`** to speak with a courtier\n"
        f"**Use `!summon [topic]`** to start a court debate\n\n"
        "*Your loyal court awaits your command, Your Majesty* 🙇"
    )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
