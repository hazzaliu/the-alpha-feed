"""
Lord Herald - Chief Intelligence Officer (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class LordHerald(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Herald",
            title="Lord Herald of Market Intelligence",
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
        self.pronouns = "he/him"
