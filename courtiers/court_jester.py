"""
The Court Jester - Chief Experience Officer
"""

from courtiers.base_courtier import BaseCourtier


class CourtJester(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Court Jester",
            title="The Court Jester",
            role="Chief Experience Officer"
        )
        self.specialties = [
            "UX review",
            "usability testing",
            "user flow critique",
            "accessibility",
            "simplification",
            "user advocacy"
        ]
