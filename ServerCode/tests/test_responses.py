"""
Module docstring goes here
"""

from bubbleScan.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

from bubbleScan.requests import ScantronListInvalidRequest

SUCCESS_VALUE = {"key": ["value1", "value2"]}
GENERIC_RESPONSE_TYPE = "Response"
GENERIC_RESPONSE_MESSAGE = "This is a response"


def test_response_success_is_true():
    """
    Test if ResponseSuccess returns True when converted to a boolean.
    """
    response = ResponseSuccess(SUCCESS_VALUE)

    assert bool(response) is True


def test_response_failure_is_false():
    """
    Test if ResponseFailure returns False when converted to a boolean.
    """
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE
    )

    assert bool(response) is False


def test_response_success_has_type_and_value():
    """
    Test if ResponseSuccess has the correct type and value.
    """
    response = ResponseSuccess(SUCCESS_VALUE)

    assert response.type == ResponseTypes.SUCCESS
    assert response.value == SUCCESS_VALUE


def test_response_failure_has_type_and_message():
    """
    Test if ResponseFailure has the correct type, message, and value.
    """
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, GENERIC_RESPONSE_MESSAGE
    )

    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == GENERIC_RESPONSE_MESSAGE
    assert response.value == {
        "type": GENERIC_RESPONSE_TYPE,
        "message": GENERIC_RESPONSE_MESSAGE,
    }


def test_response_failure_initialisation_with_exception():
    """
    Test if ResponseFailure initializes correctly with an exception.
    """
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE, Exception("Just an error message")
    )

    assert bool(response) is False
    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == "Exception: Just an error message"


def test_response_failure_from_empty_invalid_request():
    """
    Test if building a response from an empty invalid request works as expected.
    """
    response = build_response_from_invalid_request(
        ScantronListInvalidRequest()
    )

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_with_errors():
    """
    Test if building a response from an invalid request with errors works as expected.
    """
    request = ScantronListInvalidRequest()
    request.add_error("path", "Is mandatory")
    request.add_error("path", "can't be blank")

    response = build_response_from_invalid_request(request)

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: can't be blank"
