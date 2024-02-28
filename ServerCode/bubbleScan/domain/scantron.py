"""
Module representing the Scantron class in the domain.
"""

import uuid
import dataclasses

@dataclasses.dataclass
class Scantron:
    """
    Data class representing a Scantron entity.

    Attributes:
    - code: UUID, the unique identifier for the scantron.
    - first: str, the first name of the person associated with the scantron.
    - last: str, the last name of the person associated with the scantron.
    - idNumber: int, the identification number associated with the scantron.
    """

    code: uuid.UUID
    first: str
    last: str
    ID_Number: int

    @classmethod
    def from_dict(cls,d):
        """
        Class method to create a Scantron instance from a dictionary.

        :param d: dict, dictionary containing the scantron attributes.
        :return: Scantron instance.
        """
        return cls(**d)

    def to_dict(self):
        """
        Convert the Scantron instance to a dictionary.

        :return: dict, dictionary representation of the scantron.
        """
        return dataclasses.asdict(self)
