"""
The Royal Treasurer - CFO and Deal Analyzer
"""

from courtiers.base_courtier import BaseCourtier


class RoyalTreasurer(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Royal Treasurer",
            title="The Royal Treasurer",
            role="CFO and Deal Analyzer"
        )
        self.specialties = [
            "pricing strategy",
            "cost analysis",
            "unit economics",
            "fundraising",
            "financial modeling",
            "business metrics"
        ]
