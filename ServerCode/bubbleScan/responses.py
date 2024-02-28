"""
Module representing response types and classes for handling responses.
"""

class ResponseTypes:
    """
    Enumeration of response types.
    """
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"


class ResponseFailure:
    """
    Class representing a failure response.

    Attributes:
    - type: str, the type of the response.
    - message: str, the formated error message.
    """
    def __init__(self, type_, message):
        """
        Initialize the ResponseFailure instance.

        :param type_: str, the type of the response.
        :param message: str or Exception, the error message or exception.
        """

        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        """
        Format the error message.

        :param msg: str or Exception, the error message or exception.
        :return: str, the formatted error message.
        """
        if isinstance(msg, Exception):
            return "{}: {}".format(
                msg.__class__.__name__, "{}".format(msg)
            )
        return msg

    @property
    def value(self):
        """
        Get the value of the response.

        :return: dict, the response value.
        """
        return {"type": self.type, "message": self.message}

    def __bool__(self):
        """
        Override the boolean conversion.

        :return: bool, False.
        """
        return False


class ResponseSuccess:
    """
    Class representing a success response. 

    Attributes: 
    - type: str, the type of the response (always "Success").
    - value: any, the value of the response.
    """
    def __init__(self, value=None):
        """
        Initialize the ResponseSuccess instance.

        :param value: any, the value of the response.
        """
        self.type = ResponseTypes.SUCCESS
        self.value = value

    def __bool__(self):
        """
        Override the boolean conversion.

        :return: bool, True.
        """
        return True


def build_response_from_invalid_request(invalid_request):
    """
    Build a failure response from an invalid request.

    :param invalid_request: ScantronListInvalidRequest, the invalid request.
    :return: ResponseFailure, the failure response.
    """
    message = "\n".join(
        [
            "{}: {}".format(err["parameter"], err["message"])
            for err in invalid_request.errors
        ]
    )
    return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, message)
