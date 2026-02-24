"""
The Court Herald - Chief Intelligence Officer (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class CourtHerald(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Court Herald",
            title="The Court Herald",
            role="Chief Intelligence Officer"
        )
        self.specialties = [
            "product trends",
            "competitor analysis",
            "market intelligence",
            "viral products",
            "tech news",
            "industry shifts"
        ]
        self.has_web_search = True
