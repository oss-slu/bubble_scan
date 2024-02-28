"""
Module representing request objects for scantron list use case.
"""

from collections.abc import Mapping

class ScantronListInvalidRequest:
    """
    Invalid request class for handling errors in scantron list requests.

    Attributes:
    - errors: list, a list of error messages.
    """
    def __init__(self):
        """
        Initialize the ScantronListInvalidRequest instance.
        """
        self.errors = []

    def add_error(self, parameter, message):
        """
        Add an error to the list of errors.

        :param parameter: str, the parameter related to the error.
        :param message: str, the error message.
        """
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        """
        Check if there are any errors.

        :return: bool, True if there are errors, False otherwise.
        """
        return len(self.errors) > 0

    def __bool__(self):
        """
        Override the boolean conversion.

        :return: bool, False.
        """
        return False
    
class ScantronListValidRequest:
    """
    Valid request class for scantron list requests.

    Attributes:
    - filters: dict or None, the filters to be applied.
    """
    def __init__(self, filters=None):
        """
        Initialize the ScantronListValidRequest instance.

        :param filters: dict or None, the filters to be applied.
        """
        self.filters = filters

    def __bool__(self):
        """
        Override the boolean conversion.

        :return: bool, True.
        """
        return True

def build_scantron_list_request(filters=None):
    """
    Build a scantron list request object.

    :param filters: dict or None, the filters to be applied.
    :return: ScantronListInvalidRequest or ScantronListValidRequest, the request object.
    """
    accepted_filters = ["code__eq", "first__eq", "last__lt", "idNumber__gt"]
    invalid_req = ScantronListInvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error("filters", "Is not iterable")
            return invalid_req

        for key, value in filters.items():
            if key not in accepted_filters:
                invalid_req.add_error(
                    "filters", "Key {} cannot be used".format(key)
                )

        if invalid_req.has_errors():
            return invalid_req

    return ScantronListValidRequest(filters=filters)
