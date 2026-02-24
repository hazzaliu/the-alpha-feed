"""
Lord Sage - Chief Product Officer
"""

from courtiers.base_courtier import BaseCourtier


class LordSage(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Sage",
            title="Lord Sage of Strategic Foresight",
            role="Chief Product Officer"
        )
        self.specialties = [
            "product strategy",
            "roadmap planning",
            "prioritization",
            "competitive moats",
            "vision alignment",
            "long-term thinking"
        ]
        self.pronouns = "he/him"
