from typing import List, Tuple, Any

from enum import Enum


class ChoiceEnum(Enum):
    """Base class for user enums."""
    @classmethod
    def choices(cls) -> List[Tuple[Any, Any]]:
        """Choose to what group user belongs to.

        Returns:
            choices (list): Choices that user have to be a part of.
        """
        choices = [(choice.name, choice.value) for choice in cls]
        return choices


class Companies(ChoiceEnum):
    """User when registering type EXPERT if employer of one of companies."""
    WINGS = "wings-ict-solutions.eu"
    INTRA = "intrasoft-intl.com"
    AUA = "aua.gr"
    DLO = "wur.nl"
    IPMS = "ipms.fraunhofer.de"
    CNR = "cnr.it"
    UTOV = "ing.uniroma2.it"
    FUB = "fu-berlin.de"
    VLF = "vizlore.com"
    OTHER = "OTHER"


class Types(ChoiceEnum):
    """User permissions thru platform."""
    BASIC = "BASIC"
    EXPERT = "EXPERT"
