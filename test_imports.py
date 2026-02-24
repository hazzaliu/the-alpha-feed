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
    
    print("✓ courtiers.lord_sebastian")
    from courtiers.lord_sebastian import LordSebastian
    
    print("✓ courtiers.lady_beatrice")
    from courtiers.lady_beatrice import LadyBeatrice
    
    print("✓ courtiers.lord_edmund")
    from courtiers.lord_edmund import LordEdmund
    
    print("✓ courtiers.lady_arabella")
    from courtiers.lady_arabella import LadyArabella
    
    print("✓ courtiers.lady_philippa")
    from courtiers.lady_philippa import LadyPhilippa
    
    print("✓ courtiers.lord_alistair")
    from courtiers.lord_alistair import LordAlistair
    
    print("✓ courtiers.lady_genevieve")
    from courtiers.lady_genevieve import LadyGenevieve
    
    # Test instantiation
    print("\nTesting courtier instantiation...")
    courtiers = {
        "lord_sebastian": LordSebastian(),
        "lady_beatrice": LadyBeatrice(),
        "lord_edmund": LordEdmund(),
        "lady_arabella": LadyArabella(),
        "lady_philippa": LadyPhilippa(),
        "lord_alistair": LordAlistair(),
        "lady_genevieve": LadyGenevieve(),
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
