"""
The Girlboss — orchestrator.
Runs the full pipeline: The Plug → That Girl → The Bestie → The Group Chat → The Content Creator.
Returns the final Discord post string and logs everything to Supabase.
"""

import traceback
from agents import the_plug, that_girl, the_bestie, the_group_chat, the_content_creator
from db.supabase_client import save_drop


def run_pipeline(drop_type: str = "PRE-MARKET") -> str:
    """
    Executes the full Alpha Feed pipeline.
    drop_type: "PRE-MARKET" or "POST-MARKET"
    Returns the final Discord post string.
    Raises on unrecoverable failure.
    """
    print(f"\n[The Girlboss] Starting {drop_type} pipeline...")

    # Step 1: The Plug — fetch headlines
    try:
        headlines = the_plug.run()
    except Exception as e:
        print(f"[The Girlboss] The Plug failed: {e}")
        traceback.print_exc()
        raise RuntimeError("The Plug couldn't get the news bestie, something's cooked with the feeds 💀") from e

    if not headlines:
        print("[The Girlboss] No new headlines found.")
        return (
            "✨ **THE ALPHA FEED** ✨\n\n"
            "> bestie... nothing new dropped today. markets are in their quiet era 😴\n\n"
            "*this is for educational purposes only and NOT financial advice bestie. "
            "talk to an actual financial advisor before you do anything with your money fr 🙏*"
        )

    # Step 2: That Girl — financial analysis
    try:
        analysis = that_girl.run(headlines)
    except Exception as e:
        print(f"[The Girlboss] That Girl failed: {e}")
        traceback.print_exc()
        raise RuntimeError("That Girl's analysis flopped, the AI is having a moment 😵") from e

    # Step 3: The Bestie — fact check
    try:
        checked = the_bestie.run(analysis)
    except Exception as e:
        print(f"[The Girlboss] The Bestie failed, using That Girl's raw output: {e}")
        checked = analysis

    # Step 4: The Group Chat — Gen Z translation
    try:
        translated = the_group_chat.run(checked)
    except Exception as e:
        print(f"[The Girlboss] The Group Chat failed: {e}")
        traceback.print_exc()
        raise RuntimeError("The Group Chat is offline, translation failed fr 😭") from e

    # Step 5: The Content Creator — Discord formatting
    try:
        post = the_content_creator.run(translated, drop_type=drop_type)
    except Exception as e:
        print(f"[The Girlboss] The Content Creator failed: {e}")
        traceback.print_exc()
        raise RuntimeError("The Content Creator couldn't format the post, aesthetic crisis 💅") from e

    # Log to Supabase
    try:
        save_drop(
            raw_json={
                "headlines_count": len(headlines),
                "analysis": analysis,
                "checked": checked,
                "translated": translated,
                "drop_type": drop_type,
            },
            final_text=post,
        )
        print("[The Girlboss] Drop saved to Supabase.")
    except Exception as e:
        print(f"[The Girlboss] Supabase save failed (non-critical): {e}")

    print("[The Girlboss] Pipeline complete. Drop ready.")
    return post
