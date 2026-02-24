"""
Lord Sebastian, Grand Architect - Chief Engineer and Technical Advisor
"""

from courtiers.base_courtier import BaseCourtier


class LordSebastian(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Sebastian",
            title="Lord Sebastian, Grand Architect",
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
        self.nickname = "Seb"
