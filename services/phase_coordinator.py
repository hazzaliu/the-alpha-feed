"""
Phase-based coordination system for Lady Philippa.
Breaks complex tasks into structured phases to avoid conversation chaos.
"""

import discord
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class PhaseStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"


@dataclass
class Phase:
    """Represents a single phase in a multi-phase task."""
    name: str
    description: str
    assigned_courtiers: List[str]  # List of courtier keys (e.g., "lord_sebastian")
    deliverables: List[str]
    status: PhaseStatus = PhaseStatus.PENDING
    responses: Dict[str, str] = None  # courtier_key -> response
    synthesis: Optional[str] = None
    
    def __post_init__(self):
        if self.responses is None:
            self.responses = {}


@dataclass
class CoordinatedTask:
    """Represents a multi-phase coordinated task."""
    task_id: str
    task_name: str
    phases: List[Phase]
    current_phase_index: int = 0
    thread: Optional[discord.Thread] = None
    emperor_user_id: str = None
    
    @property
    def current_phase(self) -> Optional[Phase]:
        if 0 <= self.current_phase_index < len(self.phases):
            return self.phases[self.current_phase_index]
        return None
    
    @property
    def is_complete(self) -> bool:
        return self.current_phase_index >= len(self.phases)
    
    def advance_phase(self):
        """Move to the next phase."""
        self.current_phase_index += 1


class PhaseCoordinator:
    """
    Manages phase-based coordination for complex tasks.
    Ensures courtiers respond in order, one phase at a time.
    """
    
    def __init__(self):
        self.active_tasks: Dict[int, CoordinatedTask] = {}  # thread_id -> task
    
    def create_task(
        self,
        thread: discord.Thread,
        task_name: str,
        phases: List[Phase],
        emperor_user_id: str
    ) -> CoordinatedTask:
        """Create a new coordinated task."""
        task = CoordinatedTask(
            task_id=str(thread.id),
            task_name=task_name,
            phases=phases,
            thread=thread,
            emperor_user_id=emperor_user_id
        )
        self.active_tasks[thread.id] = task
        return task
    
    def get_task(self, thread_id: int) -> Optional[CoordinatedTask]:
        """Get an active task by thread ID."""
        return self.active_tasks.get(thread_id)
    
    def is_courtier_allowed_to_respond(
        self,
        thread_id: int,
        courtier_key: str
    ) -> bool:
        """Check if a courtier is allowed to respond in the current phase."""
        task = self.get_task(thread_id)
        if not task:
            return True  # No active task, allow response
        
        current_phase = task.current_phase
        if not current_phase:
            return False  # Task complete, no more responses
        
        # Check if this courtier is assigned to current phase
        return courtier_key in current_phase.assigned_courtiers
    
    def record_response(
        self,
        thread_id: int,
        courtier_key: str,
        response: str
    ):
        """Record a courtier's response for the current phase."""
        task = self.get_task(thread_id)
        if not task or not task.current_phase:
            return
        
        task.current_phase.responses[courtier_key] = response
        
        # Check if all assigned courtiers have responded
        if self.is_phase_complete(thread_id):
            task.current_phase.status = PhaseStatus.COMPLETED
    
    def is_phase_complete(self, thread_id: int) -> bool:
        """Check if all courtiers in current phase have responded."""
        task = self.get_task(thread_id)
        if not task or not task.current_phase:
            return False
        
        phase = task.current_phase
        return all(
            courtier in phase.responses
            for courtier in phase.assigned_courtiers
        )
    
    def get_phase_summary(self, thread_id: int) -> Optional[str]:
        """Get a summary of the current phase for Philippa to synthesize."""
        task = self.get_task(thread_id)
        if not task or not task.current_phase:
            return None
        
        phase = task.current_phase
        summary = f"PHASE: {phase.name}\n\n"
        
        for courtier_key, response in phase.responses.items():
            courtier_name = courtier_key.replace("_", " ").title()
            summary += f"{courtier_name}:\n{response}\n\n"
        
        return summary
    
    def approve_phase(self, thread_id: int):
        """Mark current phase as approved and advance to next."""
        task = self.get_task(thread_id)
        if not task or not task.current_phase:
            return
        
        task.current_phase.status = PhaseStatus.APPROVED
        task.advance_phase()
        
        # Start next phase if it exists
        if task.current_phase:
            task.current_phase.status = PhaseStatus.IN_PROGRESS
    
    def get_task_status(self, thread_id: int) -> Optional[str]:
        """Get a formatted status update for the task."""
        task = self.get_task(thread_id)
        if not task:
            return None
        
        status = f"📊 TASK STATUS: {task.task_name}\n\n"
        
        for i, phase in enumerate(task.phases):
            if i < task.current_phase_index:
                status += f"✅ Phase {i+1}: {phase.name} (COMPLETED)\n"
            elif i == task.current_phase_index:
                completed = len(phase.responses)
                total = len(phase.assigned_courtiers)
                status += f"⏳ Phase {i+1}: {phase.name} (IN PROGRESS - {completed}/{total} courtiers responded)\n"
            else:
                status += f"⬜ Phase {i+1}: {phase.name} (PENDING)\n"
        
        if task.is_complete:
            status += "\n🎉 ALL PHASES COMPLETE!"
        
        return status
    
    def cleanup_task(self, thread_id: int):
        """Remove a completed task from active tasks."""
        if thread_id in self.active_tasks:
            del self.active_tasks[thread_id]


# Global instance
_phase_coordinator = PhaseCoordinator()


def get_phase_coordinator() -> PhaseCoordinator:
    """Get the global phase coordinator instance."""
    return _phase_coordinator
