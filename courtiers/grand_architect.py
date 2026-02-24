"""
The Grand Architect - Chief Engineer and Technical Advisor
"""

from courtiers.base_courtier import BaseCourtier


class GrandArchitect(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Grand Architect",
            title="The Grand Architect",
            role="Chief Engineer and Technical Advisor"
        )
        self.specialties = [
            "architecture design",
            "code review",
            "tech stack selection",
            "debugging",
            "performance optimization",
            "best practices"
        ]
