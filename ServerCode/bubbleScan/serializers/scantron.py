"""
Module representing a JSON encoder for the Scantron class.
"""
import json

class ScantronJsonEncoder(json.JSONEncoder):
    """
    JSON encoder for the Scantron class.

    Methods:
    - default(o): Override the default method to handle Scantron instances.

    Attributes:
    - None
    """
    def default(self, o):
        """
        Override the default method to handle Scantron instances.

        :param o: any, the object to encode.
        :return: dict, the serialized representation of the Scantron object.
        """
        try:
            to_serialize = {
                "code": str(o.code),
                "first": o.first,
                "last": o.last,
                "idNumber": o.idNumber,
			}
            return to_serialize
        except AttributeError: 
            return super().default(o)
