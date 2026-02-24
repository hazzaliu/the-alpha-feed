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
    
    print("✓ courtiers.grand_architect")
    from courtiers.grand_architect import GrandArchitect
    
    print("✓ courtiers.royal_treasurer")
    from courtiers.royal_treasurer import RoyalTreasurer
    
    print("✓ courtiers.court_herald")
    from courtiers.court_herald import CourtHerald
    
    print("✓ courtiers.royal_envoy")
    from courtiers.royal_envoy import RoyalEnvoy
    
    print("✓ courtiers.grand_vizier")
    from courtiers.grand_vizier import GrandVizier
    
    print("✓ courtiers.royal_sage")
    from courtiers.royal_sage import RoyalSage
    
    print("✓ courtiers.court_jester")
    from courtiers.court_jester import CourtJester
    
    # Test instantiation
    print("\nTesting courtier instantiation...")
    courtiers = {
        "grand_architect": GrandArchitect(),
        "royal_treasurer": RoyalTreasurer(),
        "court_herald": CourtHerald(),
        "royal_envoy": RoyalEnvoy(),
        "grand_vizier": GrandVizier(),
        "royal_sage": RoyalSage(),
        "court_jester": CourtJester(),
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
