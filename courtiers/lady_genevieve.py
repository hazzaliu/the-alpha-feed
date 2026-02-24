"""
Lady Genevieve, Court Jester - Chief Experience Officer
"""

from courtiers.base_courtier import BaseCourtier


class LadyGenevieve(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Genevieve",
            title="Lady Genevieve, Court Jester",
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
        self.pronouns = "she/her"
        self.nickname = "Genny"
