"""
Module representing the use case for listing scantrons.
"""

from bubbleScan.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_from_invalid_request,
)

def scantron_list_use_case(repo, request):
    """
    Use case for listing scantrons.

    :param repo: Repository, the repository for accessing scantron data.
    :param request: ScantronListValidRequest, the request object containing filters.
    :return: ResponseSuccess or ResponseFailure, the appropriate response object.
    """
    if not request:
        return build_response_from_invalid_request(request)
    try:
        rooms = repo.list(filters=request.filters)
        return ResponseSuccess(rooms)
    except Exception as exc:
        print(f"An exception occurred: {exc}")
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, f"An unexpected error occurred.: {exc}")
