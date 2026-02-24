"""
The Royal Sage - Chief Product Officer
"""

from courtiers.base_courtier import BaseCourtier


class RoyalSage(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Royal Sage",
            title="The Royal Sage",
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
