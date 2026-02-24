"""
Task Coordinator - Lady Philippa orchestrates multi-courtier tasks and reports back to the Emperor.
"""

import discord
from typing import List, Dict, Optional
from courtiers.base_courtier import BaseCourtier


class TaskCoordinator:
    """
    Handles complex tasks where Lady Philippa coordinates multiple courtiers.
    The Emperor gives high-level instructions, Philippa breaks it down, 
    assigns courtiers, and synthesizes their work into a final report.
    """
    
    def __init__(self, channel: discord.TextChannel, courtiers: Dict[str, BaseCourtier]):
        self.channel = channel
        self.courtiers = courtiers
        self.active_tasks: Dict[int, dict] = {}  # thread_id -> task state
    
    async def start_task(
        self,
        initial_message: discord.Message,
        task_description: str,
        emperor_message: str
    ) -> discord.Thread:
        """
        Start a coordinated task where Philippa orchestrates multiple courtiers.
        
        Args:
            initial_message: The Emperor's message
            task_description: Brief description for thread name
            emperor_message: The Emperor's full request
        
        Returns:
            The created Discord thread
        """
        # Create thread for the task
        thread = await initial_message.create_thread(
            name=f"Task: {task_description[:80]}",
            auto_archive_duration=1440  # 24 hours
        )
        
        # Initialize task state
        self.active_tasks[thread.id] = {
            "task": task_description,
            "emperor_request": emperor_message,
            "courtier_outputs": {},
            "status": "planning",
            "history": []
        }
        
        # Lady Philippa analyzes the task and creates a plan
        vizier = self.courtiers.get("lady_philippa")
        if not vizier:
            await thread.send("Error: Grand Vizier not available")
            return thread
        
        # Philippa breaks down the task
        planning_prompt = f"""Your Majesty has requested: {emperor_message}

Your job as Grand Vizier:
1. Break this down into specific sub-tasks
2. Identify which courtiers should handle each sub-task
3. Create a coordination plan
4. Present the plan to His Majesty for approval

Format your response as:
**TASK BREAKDOWN:**
- Sub-task 1: [description]
- Sub-task 2: [description]
...

**COURTIER ASSIGNMENTS:**
- [Courtier Name]: [what they'll do]
- [Courtier Name]: [what they'll do]
...

**COORDINATION PLAN:**
[How you'll orchestrate this and when you'll report back]

Then ask His Majesty: "Does this plan work for you, Your Majesty? Say 'proceed' and I'll coordinate the court fr fr 📋"
"""
        
        plan = await vizier.respond(planning_prompt)
        await thread.send(f"**{vizier.title}**:\n{plan}")
        
        self.active_tasks[thread.id]["plan"] = plan
        self.active_tasks[thread.id]["history"].append(f"Vizier Plan: {plan}")
        
        return thread
    
    async def execute_task(
        self,
        thread: discord.Thread,
        courtier_assignments: Dict[str, str]
    ):
        """
        Execute the task by having each assigned courtier complete their part.
        
        Args:
            thread: The task thread
            courtier_assignments: Dict of courtier_key -> task description
        """
        if thread.id not in self.active_tasks:
            await thread.send("Error: No active task found")
            return
        
        task = self.active_tasks[thread.id]
        task["status"] = "executing"
        
        vizier = self.courtiers.get("lady_philippa")
        
        # Update Emperor
        await thread.send(f"**{vizier.title}**: Coordinating the court now Your Majesty... 🎯")
        
        # Execute each courtier's assignment
        for courtier_key, assignment in courtier_assignments.items():
            courtier = self.courtiers.get(courtier_key)
            if not courtier:
                continue
            
            # Show typing indicator
            async with thread.typing():
                # Build context from previous work
                context = {
                    "task": task["task"],
                    "emperor_request": task["emperor_request"],
                    "previous_work": task["courtier_outputs"]
                }
                
                # Courtier completes their assignment
                response = await courtier.respond(assignment, context)
                
                # Save output
                task["courtier_outputs"][courtier_key] = response
                task["history"].append(f"{courtier.name}: {response}")
                
                # Post to thread
                await thread.send(f"**{courtier.title}**:\n{response}\n")
        
        # Philippa synthesizes everything
        await self.synthesize_final_report(thread)
    
    async def synthesize_final_report(self, thread: discord.Thread):
        """
        Lady Philippa synthesizes all courtier work into a final report for the Emperor.
        """
        if thread.id not in self.active_tasks:
            return
        
        task = self.active_tasks[thread.id]
        task["status"] = "synthesizing"
        
        vizier = self.courtiers.get("lady_philippa")
        if not vizier:
            return
        
        # Build synthesis prompt
        synthesis_prompt = f"""Your Majesty, the court has completed the task: {task['task']}

Here's what each courtier delivered:

"""
        
        for courtier_key, output in task["courtier_outputs"].items():
            courtier = self.courtiers.get(courtier_key)
            synthesis_prompt += f"\n**{courtier.name}**:\n{output}\n"
        
        synthesis_prompt += """

Now synthesize this into a FINAL REPORT for His Majesty:

**SUMMARY:**
[What was accomplished]

**KEY DELIVERABLES:**
- [Deliverable 1]
- [Deliverable 2]
...

**RECOMMENDATIONS:**
[What His Majesty should do next]

**STATUS:**
[Is this complete or does more work need to happen?]

Keep it concise and actionable. His Majesty needs the TL;DR fr fr 📋
"""
        
        # Philippa creates final report
        async with thread.typing():
            final_report = await vizier.respond(synthesis_prompt)
        
        # Post final report with clear formatting
        await thread.send(
            f"\n{'='*50}\n"
            f"**📋 FINAL REPORT TO HIS MAJESTY 📋**\n"
            f"{'='*50}\n\n"
            f"**{vizier.title}**:\n{final_report}\n\n"
            f"*Task complete, Your Majesty. The court awaits your next command* 🙇"
        )
        
        # Mark task as complete
        task["status"] = "complete"
        task["final_report"] = final_report
    
    async def get_task_status(self, thread: discord.Thread) -> Optional[str]:
        """Get the current status of a task."""
        if thread.id not in self.active_tasks:
            return None
        return self.active_tasks[thread.id]["status"]
