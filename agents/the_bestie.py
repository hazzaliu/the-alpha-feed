"""
The Bestie — fact-checker and hype detector agent.
Receives That Girl's analysis, returns confidence-scored and cleaned JSON.
"""

import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY

_client: OpenAI | None = None

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "the_bestie.txt")


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
    Takes That Girl's analysis dict.
    Returns fact-checked, confidence-scored analysis dict.
    """
    if not analysis.get("stories"):
        return analysis

    system_prompt = _load_prompt()
    user_message = f"Here is That Girl's analysis to review:\n\n{json.dumps(analysis, indent=2)}\n\nFact-check it now."

    print("[The Bestie] Fact-checking analysis...")
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    result = json.loads(raw)
    print(f"[The Bestie] Approved {len(result.get('stories', []))} stories after review.")
    return result
