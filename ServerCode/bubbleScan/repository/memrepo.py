"""
Module representing the MemRepo class in the repository
"""

from bubbleScan.domain.scantron import Scantron

class MemRepo:
    """
    Repository class for handling Scantron entities in memory.

    Attributes:
    - data: list, the list of scantron data stored in memory.
    """
    def __init__(self,data):
        """
        Initialize the MemRepo instance

        :param data: list, the list of scantron data to be stored.
        """
        self.data = data

    def list(self):
        """
        Retrieve a list of Scantron instances from the stored data.

        :return: list, a list of Scantron instances
        """
        return [Scantron.from_dict(i) for i in self.data]

    def add_scantron(self, scantron):
        """
        Add a Scantron instance to the repository.

        :param scantron: Scantron, the Scantron instance to be added.
        """
        self.data.append(scantron.to_dict())
