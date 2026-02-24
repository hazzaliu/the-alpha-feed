"""
The Group Chat — Gen Z translator agent.
Receives The Bestie's fact-checked analysis, returns Gen Z-voiced JSON.
"""

import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY

_client: OpenAI | None = None

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "the_group_chat.txt")


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _load_prompt() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def run(analysis: dict) -> dict:
    """
    Takes The Bestie's analysis dict.
    Returns Gen Z-translated analysis dict.
    """
    if not analysis.get("stories"):
        return {
            "stories": [],
            "vibe_check": "NEUTRAL 😐",
            "vibe_summary": "nothing to report today bestie, the markets are being boring fr",
        }

    system_prompt = _load_prompt()
    user_message = f"Here is the analysis to translate into Gen Z:\n\n{json.dumps(analysis, indent=2)}\n\nTranslate it now."

    print("[The Group Chat] Translating to Gen Z...")
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    result = json.loads(raw)
    print(f"[The Group Chat] Translated {len(result.get('stories', []))} stories.")
    return result
