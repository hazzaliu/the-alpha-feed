"""
Lord Edmund, Court Herald - Chief Intelligence Officer (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class LordEdmund(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lord Edmund",
            title="Lord Edmund, Court Herald",
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
        self.nickname = "Eddie"
