-- Emperor's Court Database Schema
-- Run this in your Supabase SQL Editor to set up the database

-- 1. Conversations table (tracks each interaction with the Emperor)
create table if not exists conversations (
    id bigserial primary key,
    emperor_message_id text not null,
    thread_id text,
    context jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_conversations_created_at on conversations(created_at desc);
create index if not exists idx_conversations_thread_id on conversations(thread_id);

-- 2. Courtier responses (tracks each courtier's response in conversations)
create table if not exists courtier_responses (
    id bigserial primary key,
    conversation_id bigint references conversations(id) on delete cascade,
    courtier_name text not null,
    response_text text,
    response_json jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_courtier_responses_conversation on courtier_responses(conversation_id);
create index if not exists idx_courtier_responses_courtier on courtier_responses(courtier_name);
create index if not exists idx_courtier_responses_created_at on courtier_responses(created_at desc);

-- 3. Project context (tracks projects the Emperor is building)
create table if not exists project_context (
    id bigserial primary key,
    project_name text not null unique,
    description text,
    tech_stack jsonb,
    decisions jsonb,
    updated_at timestamptz not null default now()
);

create index if not exists idx_project_context_updated_at on project_context(updated_at desc);

-- 4. Legacy tables from Alpha Feed (keep for reference, mark as deprecated)
-- These tables were used for the old news/finance bot system

-- seen_headlines table (used for deduplication in news system)
-- Can be kept if you want to repurpose for tracking what the Court Herald has seen
create table if not exists seen_headlines (
    id bigserial primary key,
    headline_hash text not null unique,
    created_at timestamptz not null default now()
);

create index if not exists idx_seen_headlines_hash on seen_headlines(headline_hash);
create index if not exists idx_seen_headlines_created_at on seen_headlines(created_at desc);

-- drops table (used for storing published drops in news system)
-- Can be kept for historical reference
create table if not exists drops (
    id bigserial primary key,
    drop_type text,
    content text,
    created_at timestamptz not null default now()
);

create index if not exists idx_drops_created_at on drops(created_at desc);

-- Grant permissions (adjust as needed for your Supabase setup)
-- If using service_role key, you might not need these
-- If using anon/authenticated keys, you'll need RLS policies

-- Example: Allow authenticated users to read/write (adjust based on your auth setup)
-- alter table conversations enable row level security;
-- alter table courtier_responses enable row level security;
-- alter table project_context enable row level security;
