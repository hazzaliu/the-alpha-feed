"""
Lord Architect - Chief Engineer and Technical Advisor
"""

from courtiers.base_courtier import BaseCourtier


class LordArchitect(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Architect",
            title="Lord Architect of the Digital Realm",
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
        self.pronouns = "he/him"
