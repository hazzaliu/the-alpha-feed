"""
Lady Beatrice, Royal Treasurer - CFO and Deal Analyzer
"""

from courtiers.base_courtier import BaseCourtier


class LadyBeatrice(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Beatrice",
            title="Lady Beatrice, Royal Treasurer",
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
        self.nickname = "Bea"
