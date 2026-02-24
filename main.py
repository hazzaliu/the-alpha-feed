"""
The Alpha Feed — entry point.
Starts the Discord bot and APScheduler for automated drops.
"""

import asyncio
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

import orchestrator
from config import (
    DISCORD_TOKEN,
    DISCORD_CHANNEL_ID,
    SCHEDULE_PRE_MARKET_UTC,
    SCHEDULE_POST_MARKET_UTC,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler(timezone=pytz.utc)


async def post_drop(drop_type: str) -> None:
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        print(f"[main] Channel {DISCORD_CHANNEL_ID} not found.")
        return

    await channel.send(f"⏳ *The Alpha Feed is cooking up the {drop_type.lower()} drop...*")

    try:
        post = orchestrator.run_pipeline(drop_type=drop_type)
        await channel.send(post)
    except Exception as e:
        await channel.send(
            f"💀 **THE ALPHA FEED** — something went cooked in the pipeline bestie\n"
            f"```{str(e)[:300]}```\n"
            f"*we'll be back, this is just a flop era moment*"
        )
        print(f"[main] Pipeline error: {e}")


@bot.event
async def on_ready():
    print(f"[main] The Alpha Feed is online as {bot.user}")

    scheduler.add_job(
        lambda: asyncio.create_task(post_drop("PRE-MARKET")),
        CronTrigger(
            hour=SCHEDULE_PRE_MARKET_UTC["hour"],
            minute=SCHEDULE_PRE_MARKET_UTC["minute"],
            timezone=pytz.utc,
        ),
        id="pre_market",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: asyncio.create_task(post_drop("POST-MARKET")),
        CronTrigger(
            hour=SCHEDULE_POST_MARKET_UTC["hour"],
            minute=SCHEDULE_POST_MARKET_UTC["minute"],
            timezone=pytz.utc,
        ),
        id="post_market",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()

    print("[main] Scheduler started. Pre-market: 13:00 UTC | Post-market: 22:00 UTC")


@bot.command(name="drop")
async def drop_command(ctx: commands.Context, *, args: str = ""):
    """
    !drop the alpha — manually trigger the pipeline.
    Accepts optional "pre" or "post" argument to specify drop type.
    """
    args_lower = args.lower()
    if "post" in args_lower:
        drop_type = "POST-MARKET"
    else:
        drop_type = "PRE-MARKET"

    await ctx.message.add_reaction("✨")
    await post_drop(drop_type)


@bot.command(name="status")
async def status_command(ctx: commands.Context):
    """!status — check if the bot is alive."""
    await ctx.send(
        "✅ **The Alpha Feed is online bestie** 💅\n"
        "- Pre-market drop: **8:00 AM ET** daily\n"
        "- Post-market drop: **5:00 PM ET** daily\n"
        "- Manual trigger: `!drop the alpha`"
    )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
