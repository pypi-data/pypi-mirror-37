from enum import Enum


class TranscoderName(Enum):
    ELEMENTAL_JB = 0
    ATEME_JB = 1
    ATEME_EG = 2

    NAME_TO_STR = [
        'elemental-jb',
        'ateme-jb',
        'ateme-eg'
    ]

    NAME_TO_FRIENDLY_SRT = [
        'Elemental Emissora',
        'Ateme Emissora',
        'Ateme Estúdios Globo'
    ]

    def to_string(self):
        return TranscoderName.NAME_TO_STR.value[self.value]

    @staticmethod
    def from_string(status_string):
        return TranscoderName(TranscoderName.NAME_TO_STR.value.index(status_string))

    def to_friendly_string(self):
        return TranscoderName.NAME_TO_FRIENDLY_SRT.value[self.value]

    @staticmethod
    def string_to_friendly_string(status_string):
        job_status = TranscoderName.NAME_TO_STR.value.index(status_string)
        return TranscoderName.NAME_TO_FRIENDLY_SRT.value[job_status]
