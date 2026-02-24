import hashlib
from datetime import datetime, timezone
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def is_headline_seen(url: str) -> bool:
    client = get_client()
    h = url_hash(url)
    result = client.table("seen_headlines").select("id").eq("url_hash", h).limit(1).execute()
    return len(result.data) > 0


def mark_headline_seen(url: str, title: str) -> None:
    client = get_client()
    client.table("seen_headlines").insert({
        "url_hash": url_hash(url),
        "url": url,
        "title": title,
        "seen_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


def save_drop(raw_json: dict, final_text: str) -> None:
    client = get_client()
    client.table("drops").insert({
        "raw_json": raw_json,
        "final_text": final_text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


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
