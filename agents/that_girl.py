"""
That Girl — financial analyst agent.
Receives raw headlines, returns structured JSON analysis.
"""

import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY

_client: OpenAI | None = None

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "that_girl.txt")


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _load_prompt() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def run(headlines: list[dict]) -> dict:
    """
    Takes a list of headline dicts from The Plug.
    Returns a structured analysis dict.
    """
    if not headlines:
        return {"stories": [], "overall_sentiment": "NEUTRAL", "sentiment_reason": "No headlines available."}

    headlines_text = "\n".join(
        f"- [{h['source']}] {h['title']}: {h.get('description', '')}"
        for h in headlines
    )

    system_prompt = _load_prompt()
    user_message = f"Here are today's headlines:\n\n{headlines_text}\n\nProduce your analysis now."

    print("[That Girl] Analyzing headlines...")
    response = _get_client().chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    result = json.loads(raw)
    print(f"[That Girl] Produced {len(result.get('stories', []))} stories.")
    return result
