"""
One-time database setup script.
Run this locally once to create the Supabase tables.

Usage:
    python setup_db.py

Alternatively, paste the SQL below directly into the Supabase SQL Editor:
https://supabase.com/dashboard/project/dezofblswtukueblxtli/sql
"""

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

SCHEMA_SQL = """
create table if not exists seen_headlines (
    id bigserial primary key,
    url_hash text not null unique,
    url text not null,
    title text,
    seen_at timestamptz not null default now()
);

create table if not exists drops (
    id bigserial primary key,
    raw_json jsonb,
    final_text text,
    created_at timestamptz not null default now()
);
"""

print("Connecting to Supabase...")
client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\nCould not run DDL via REST API directly.")
print("Please run the following SQL in the Supabase SQL Editor:")
print(f"https://supabase.com/dashboard/project/dezofblswtukueblxtli/sql/new")
print("\n" + "=" * 60)
print(SCHEMA_SQL)
print("=" * 60)
print("\nAfter running the SQL, your tables will be ready.")
