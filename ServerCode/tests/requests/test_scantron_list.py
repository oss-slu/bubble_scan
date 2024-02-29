"""
Module: test_scantron list

This module contains unit tests for the 'build_scantron_list_request' function.
"""

import pytest

from bubbleScan.requests.scantron_list import build_scantron_list_request

def test_build_scantron_list_request_without_parameters():
    """
    Test the 'build_scantron_list_request' function without parameters.
    """
    request = build_scantron_list_request()

    assert request.filters is None
    assert bool(request) is True

def test_build_scantron_list_request_from_empty_dict():
    """
    Test the 'build_scantron_list_request' function with an empty dictionary.
    """
    request = build_scantron_list_request({})

    assert request.filters == {}
    assert bool(request) is True

@pytest.mark.parametrize(
    "key", ["code__eq", "first__eq", "last__lt", "idNumber__gt"]
)
def test_build_scantron_list_request_accepted_filters(key):
    """
    Test the 'build_scantron_list_request' function with accepted filters.
    """
    filters = {key: 1}

    request = build_scantron_list_request(filters=filters)

    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["code__lt", "code__gt"])
def test_build_scantron_list_request_rejected_filters(key):
    """
    Test the 'build_scantron_list_request' function with rejected filters.
    """
    filters = {key: 1}

    request = build_scantron_list_request(filters=filters)

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False
