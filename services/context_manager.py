"""
Context manager - handles Supabase storage and retrieval for conversations and project context.
"""

from typing import Dict, List, Optional
from db.supabase_client import get_supabase_client


async def save_conversation(emperor_message_id: str, thread_id: Optional[str] = None, context: Optional[Dict] = None) -> int:
    """
    Save a new conversation to Supabase.
    
    Returns the conversation ID.
    """
    supabase = get_supabase_client()
    
    data = {
        "emperor_message_id": emperor_message_id,
        "thread_id": thread_id,
        "context": context or {}
    }
    
    result = supabase.table("conversations").insert(data).execute()
    return result.data[0]["id"]


async def save_courtier_response(conversation_id: int, courtier_name: str, response_text: str, response_json: Optional[Dict] = None):
    """Save a courtier's response to a conversation."""
    supabase = get_supabase_client()
    
    data = {
        "conversation_id": conversation_id,
        "courtier_name": courtier_name,
        "response_text": response_text,
        "response_json": response_json
    }
    
    supabase.table("courtier_responses").insert(data).execute()


async def get_conversation_history(conversation_id: int) -> List[Dict]:
    """Retrieve all courtier responses for a conversation."""
    supabase = get_supabase_client()
    
    result = supabase.table("courtier_responses")\
        .select("*")\
        .eq("conversation_id", conversation_id)\
        .order("created_at")\
        .execute()
    
    return result.data


async def get_recent_conversations(emperor_user_id: str, limit: int = 10) -> List[Dict]:
    """Get recent conversations for context."""
    supabase = get_supabase_client()
    
    result = supabase.table("conversations")\
        .select("*, courtier_responses(*)")\
        .order("created_at", desc=True)\
        .limit(limit)\
        .execute()
    
    return result.data


async def save_project_context(project_name: str, description: str, tech_stack: Optional[Dict] = None, decisions: Optional[Dict] = None):
    """Save or update project context."""
    supabase = get_supabase_client()
    
    # Check if project exists
    existing = supabase.table("project_context")\
        .select("id")\
        .eq("project_name", project_name)\
        .execute()
    
    data = {
        "project_name": project_name,
        "description": description,
        "tech_stack": tech_stack or {},
        "decisions": decisions or {}
    }
    
    if existing.data:
        # Update existing
        supabase.table("project_context")\
            .update(data)\
            .eq("project_name", project_name)\
            .execute()
    else:
        # Insert new
        supabase.table("project_context").insert(data).execute()


async def get_project_context(project_name: str) -> Optional[Dict]:
    """Retrieve project context by name."""
    supabase = get_supabase_client()
    
    result = supabase.table("project_context")\
        .select("*")\
        .eq("project_name", project_name)\
        .execute()
    
    return result.data[0] if result.data else None


async def list_projects() -> List[Dict]:
    """List all tracked projects."""
    supabase = get_supabase_client()
    
    result = supabase.table("project_context")\
        .select("project_name, description, updated_at")\
        .order("updated_at", desc=True)\
        .execute()
    
    return result.data
