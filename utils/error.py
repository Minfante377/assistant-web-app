from consts import ErrorMap


def error_map(status_code):
    """
    This function maps status codes to user friendly errors.

    Args:
        - status_code(int):

    Returns(str):

    """
    return ErrorMap.USER_ERRORS[str(status_code)]
