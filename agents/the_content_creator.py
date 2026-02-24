"""
The Content Creator — Discord formatter agent.
Receives The Group Chat's Gen Z analysis, returns a formatted Discord message string.
"""

import json
import os
from datetime import datetime, timezone
from openai import OpenAI
from config import OPENAI_API_KEY

_client: OpenAI | None = None

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "the_content_creator.txt")


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _load_prompt() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def run(analysis: dict, drop_type: str = "PRE-MARKET") -> str:
    """
    Takes The Group Chat's Gen Z analysis dict and drop_type ("PRE-MARKET" or "POST-MARKET").
    Returns a formatted Discord message string ready to post.
    """
    if not analysis.get("stories"):
        today = datetime.now(timezone.utc).strftime("%A, %b %d")
        return (
            f"✨ **THE ALPHA FEED** ✨\n"
            f"📅 {today} | {drop_type} Drop\n\n"
            f"> nothing popped off today bestie, markets said nothing to report 😴\n\n"
            f"*this is for educational purposes only and NOT financial advice bestie. "
            f"talk to an actual financial advisor before you do anything with your money fr 🙏*"
        )

    system_prompt = _load_prompt()
    today = datetime.now(timezone.utc).strftime("%A, %b %d")
    user_message = (
        f"Today's date: {today}\n"
        f"Drop type: {drop_type}\n\n"
        f"Here is the Gen Z analysis to format:\n\n{json.dumps(analysis, indent=2)}\n\n"
        f"Format it into the Discord post now."
    )

    print("[The Content Creator] Formatting Discord post...")
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.5,
    )

    post = response.choices[0].message.content.strip()

    if len(post) > 1900:
        post = post[:1897] + "..."

    print(f"[The Content Creator] Post ready ({len(post)} chars).")
    return post
