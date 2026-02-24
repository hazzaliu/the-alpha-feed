"""
Lady Vizier - Chief of Staff and Requirement Gatherer
"""

from courtiers.base_courtier import BaseCourtier


class LadyVizier(BaseCourtier):
    def __init__(self):
        super().__init__(
            name="Lady Vizier",
            title="Lady Vizier of Imperial Affairs",
            role="Chief of Staff and Requirement Gatherer"
        )
        self.specialties = [
            "project coordination",
            "requirement gathering",
            "task breakdown",
            "progress tracking",
            "cross-functional orchestration",
            "clarifying questions"
        ]
        self.can_summon_others = True
        self.pronouns = "she/her"
