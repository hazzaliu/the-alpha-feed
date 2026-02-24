#!/usr/bin/env python3
"""
Quick test script to verify all imports work and courtiers can be instantiated.
Run this locally before deploying to catch import errors early.
"""

import sys

print("Testing imports...")

try:
    # Test config
    print("✓ config")
    from config import DISCORD_TOKEN, OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY
    
    # Test database
    print("✓ db.supabase_client")
    from db.supabase_client import get_supabase_client
    
    # Test services (skip debate_engine since it requires discord)
    print("✓ services.web_search")
    from services.web_search import web_search, format_search_results
    
    print("✓ services.context_manager")
    from services.context_manager import save_conversation, save_courtier_response
    
    print("⊘ services.debate_engine (skipped - requires discord.py)")
    # from services.debate_engine import DebateEngine
    
    # Test courtiers
    print("✓ courtiers.base_courtier")
    from courtiers.base_courtier import BaseCourtier
    
    print("✓ courtiers.lord_architect")
    from courtiers.lord_architect import LordArchitect
    
    print("✓ courtiers.lady_treasurer")
    from courtiers.lady_treasurer import LadyTreasurer
    
    print("✓ courtiers.lord_herald")
    from courtiers.lord_herald import LordHerald
    
    print("✓ courtiers.lady_envoy")
    from courtiers.lady_envoy import LadyEnvoy
    
    print("✓ courtiers.lady_vizier")
    from courtiers.lady_vizier import LadyVizier
    
    print("✓ courtiers.lord_sage")
    from courtiers.lord_sage import LordSage
    
    print("✓ courtiers.lady_jester")
    from courtiers.lady_jester import LadyJester
    
    # Test instantiation
    print("\nTesting courtier instantiation...")
    courtiers = {
        "lord_architect": LordArchitect(),
        "lady_treasurer": LadyTreasurer(),
        "lord_herald": LordHerald(),
        "lady_envoy": LadyEnvoy(),
        "lady_vizier": LadyVizier(),
        "lord_sage": LordSage(),
        "lady_jester": LadyJester(),
    }
    
    for key, courtier in courtiers.items():
        print(f"✓ {courtier.name} ({courtier.role})")
    
    print("\n🎉 All imports successful!")
    print(f"✅ {len(courtiers)} courtiers ready to serve")
    print("\nNote: This test skips discord-dependent modules (debate_engine, main.py)")
    print("These will be tested when deployed to Railway with full dependencies.")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
