"""
The Royal Envoy - Marketing & Growth Strategist (with web search)
"""

from courtiers.base_courtier import BaseCourtier


class RoyalEnvoy(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Royal Envoy",
            title="The Royal Envoy",
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
