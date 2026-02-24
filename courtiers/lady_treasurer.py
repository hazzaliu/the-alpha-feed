"""
Lady Treasurer - CFO and Deal Analyzer
"""

from courtiers.base_courtier import BaseCourtier


class LadyTreasurer(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Treasurer",
            title="Lady Treasurer of the Imperial Coffers",
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
        self.pronouns = "she/her"
