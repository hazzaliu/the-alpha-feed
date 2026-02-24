"""
Lord Alistair, Royal Sage - Chief Product Officer
"""

from courtiers.base_courtier import BaseCourtier


class LordAlistair(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Alistair",
            title="Lord Alistair, Royal Sage",
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
        self.nickname = "Ali"
