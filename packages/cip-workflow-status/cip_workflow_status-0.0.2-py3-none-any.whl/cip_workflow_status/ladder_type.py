from enum import Enum


class LadderType(Enum):
    AQ = 0
    AP = 1
    AQ4K = 2
    AP4K = 3

    LADDER_TO_STR = [
        "AQ",
        "AP",
        "AQ4K",
        "AP4K"
    ]

    LADDER_TO_FRIENDLY_STR = [
        "ALTA QUALIDADE",
        "ALTA PRIORIDADE",
        "ALTA QUALIDADE 4K",
        "ALTA PRIORIDADE 4K"
    ]

    def to_string(self):
        return LadderType.LADDER_TO_STR.value[self.value]

    def to_friendly_string(self):
        return LadderType.LADDER_TO_FRIENDLY_STR.value[self.value]

    @staticmethod
    def from_string(ladder_string):
        return LadderType(LadderType.LADDER_TO_STR.value.index(ladder_string))

