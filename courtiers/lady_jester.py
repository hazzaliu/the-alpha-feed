"""
Lady Jester - Chief Experience Officer
"""

from courtiers.base_courtier import BaseCourtier


class LadyJester(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Jester",
            title="Lady Jester of User Experience",
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
