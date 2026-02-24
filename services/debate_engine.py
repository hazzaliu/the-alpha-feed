"""
Debate engine - handles multi-courtier conversations in Discord threads.
"""

import discord
from typing import List, Dict
from courtiers.base_courtier import BaseCourtier


class DebateEngine:
    """Manages multi-courtier debates in Discord threads."""
    
    def __init__(self, channel: discord.TextChannel):
        self.channel = channel
        self.active_debates: Dict[int, dict] = {}  # thread_id -> debate state
    
    async def start_debate(
        self,
        initial_message: discord.Message,
        courtiers: List[BaseCourtier],
        topic: str,
        context: Dict = None
    ) -> discord.Thread:
        """
        Start a debate thread with multiple courtiers.
        
        Args:
            initial_message: The Emperor's message that triggered the debate
            courtiers: List of courtiers to participate
            topic: The debate topic/question
            context: Optional context for the debate
        
        Returns:
            The created Discord thread
        """
        # Create a thread for the debate
        thread = await initial_message.create_thread(
            name=f"Court Debate: {topic[:80]}",
            auto_archive_duration=60
        )
        
        # Initialize debate state
        self.active_debates[thread.id] = {
            "courtiers": courtiers,
            "topic": topic,
            "context": context or {},
            "history": [],
            "turn_count": 0
        }
        
        # Opening statement from Vizier if present
        vizier = next((c for c in courtiers if c.name == "Lady Vizier"), None)
        if vizier:
            opening = await vizier.respond(
                f"Your Majesty has summoned the court to discuss: {topic}\n\nLet us begin the deliberation.",
                context
            )
            await thread.send(f"**{vizier.title}**: {opening}")
            self.active_debates[thread.id]["history"].append(f"{vizier.name}: {opening}")
        
        return thread
    
    async def courtier_speaks(
        self,
        thread: discord.Thread,
        courtier: BaseCourtier,
        prompt: str = None
    ) -> str:
        """
        Have a courtier contribute to the debate.
        
        Args:
            thread: The debate thread
            courtier: The courtier speaking
            prompt: Optional specific prompt (if None, uses debate history)
        
        Returns:
            The courtier's response
        """
        if thread.id not in self.active_debates:
            return "This debate has ended."
        
        debate = self.active_debates[thread.id]
        
        # Build context from debate history
        context = debate["context"].copy()
        context["conversation_history"] = debate["history"]
        context["topic"] = debate["topic"]
        
        # Generate response
        message = prompt or f"Considering the discussion so far about '{debate['topic']}', provide your expert perspective."
        response = await courtier.respond(message, context)
        
        # Update debate state
        debate["history"].append(f"{courtier.name}: {response}")
        debate["turn_count"] += 1
        
        # Send to Discord
        await thread.send(f"**{courtier.title}**: {response}")
        
        return response
    
    async def conduct_debate_round(self, thread: discord.Thread) -> List[str]:
        """
        Have all courtiers in the debate speak once in order.
        
        Returns:
            List of responses from each courtier
        """
        if thread.id not in self.active_debates:
            return []
        
        debate = self.active_debates[thread.id]
        responses = []
        
        for courtier in debate["courtiers"]:
            # Skip Vizier in regular rounds (they moderate, not debate)
            if courtier.name == "Lady Vizier":
                continue
            
            response = await self.courtier_speaks(thread, courtier)
            responses.append(response)
        
        return responses
    
    async def synthesize_conclusion(self, thread: discord.Thread) -> str:
        """
        Have the Vizier synthesize the debate into a conclusion for the Emperor.
        
        Returns:
            The synthesized conclusion
        """
        if thread.id not in self.active_debates:
            return "No active debate found."
        
        debate = self.active_debates[thread.id]
        
        # Find Vizier
        vizier = next((c for c in debate["courtiers"] if c.name == "Lady Vizier"), None)
        if not vizier:
            # If no Vizier, just summarize
            return "Debate concluded. Please review the courtiers' perspectives above."
        
        # Build synthesis prompt
        context = debate["context"].copy()
        context["conversation_history"] = debate["history"]
        
        synthesis_prompt = f"""Your Majesty, the court has deliberated on: {debate['topic']}

Review all perspectives shared by the courtiers and synthesize:
1. Key consensus points
2. Important disagreements or tradeoffs
3. Recommended next steps
4. Any decisions the court believes you should make

Keep it concise and actionable."""
        
        conclusion = await vizier.respond(synthesis_prompt, context)
        
        await thread.send(f"\n**{vizier.title}** (Final Synthesis):\n{conclusion}")
        
        # Mark debate as concluded
        del self.active_debates[thread.id]
        
        return conclusion
    
    async def end_debate(self, thread: discord.Thread):
        """End a debate and clean up state."""
        if thread.id in self.active_debates:
            del self.active_debates[thread.id]
        await thread.edit(archived=True)
