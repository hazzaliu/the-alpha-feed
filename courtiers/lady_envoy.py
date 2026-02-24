"""
Lady Envoy - Marketing & Growth Strategist (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class LadyEnvoy(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Envoy",
            title="Lady Envoy of Royal Communications",
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
