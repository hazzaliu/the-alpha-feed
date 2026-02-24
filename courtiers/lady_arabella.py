"""
Lady Arabella, Royal Envoy - Marketing & Growth Strategist (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class LadyArabella(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Arabella",
            title="Lady Arabella, Royal Envoy",
            role="Marketing & Growth Strategist"
        )
        self.specialties = [
            "GTM strategy",
            "distribution channels",
            "viral mechanics",
            "positioning",
            "content strategy",
            "growth hacking"
        ]
        self.has_web_search = True
        self.pronouns = "she/her"
        self.nickname = "Bella"
