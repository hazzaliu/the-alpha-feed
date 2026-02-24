"""
Base Courtier class - all courtiers inherit from this.
"""

import os
from openai import OpenAI
from config import OPENAI_API_KEY

_client: OpenAI | None = None


def _get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


class BaseCourtier:
    """Base class for all Emperor's Court courtiers."""
    
    def __init__(self, name: str, title: str, role: str):
        self.name = name
        self.title = title
        self.role = role
        self.prompt_path = os.path.join(
            os.path.dirname(__file__), "..", "prompts", f"{name.lower().replace(' ', '_')}.txt"
        )
    
    def load_prompt(self) -> str:
        """Load the courtier's personality prompt from file."""
        try:
            with open(self.prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"You are {self.title}, {self.role} to His Imperial Majesty. Speak in Gen Z language while providing expert advice in your domain."
    
    async def respond(self, emperor_message: str, context: dict = None) -> str:
        """
        Generate a response to the Emperor's message.
        
        Args:
            emperor_message: The message from the Emperor
            context: Optional context (conversation history, project details, etc.)
        
        Returns:
            The courtier's response in Gen Z voice
        """
        system_prompt = self.load_prompt()
        
        # Build context string if provided
        context_str = ""
        if context:
            if context.get("conversation_history"):
                # Handle both string and list formats
                history = context["conversation_history"]
                if isinstance(history, str):
                    context_str += f"\n\n[RECENT CONVERSATION ABOVE]:\n{history}\n[END OF CONVERSATION HISTORY]\n"
                elif isinstance(history, list):
                    context_str += "\n\n[RECENT CONVERSATION ABOVE]:\n" + "\n".join(history[-5:]) + "\n[END OF CONVERSATION HISTORY]\n"
            if context.get("project_context"):
                context_str += f"\n\nProject context: {context['project_context']}"
            if context.get("web_search_results"):
                context_str += f"\n\nWeb search results: {context['web_search_results']}"
        
        user_message = f"{context_str}\n\n[CURRENT MESSAGE]: {emperor_message}"
        
        client = _get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.8,
        )
        
        return response.choices[0].message.content.strip()
    
    def __str__(self):
        return f"{self.title} ({self.name})"
