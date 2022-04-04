from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseServerError
from django.contrib.auth import authenticate


def login_user(msg):
    """
    This function checks whether a Client or Owner exists an provides
    authentication.

    Args:
        - msg(dict):
            {
               "is_client": bool,
               "is_owner": bool,
               "email": str,
               "password": str,
            }
    Returns(tupple):
        (status_code, err_msg, user)

    """
    if msg['is_client'] and msg['is_owner']:
        err_msg = "Only one of the fields 'is_client' or 'is_owner' can be"\
            "set"
        return HttpResponseBadRequest.status_code, err_msg, None

    if not msg['is_client'] and not msg['is_owner']:
        err_msg = "One of the fields 'is_client' or 'is_owner' should be set"
        return HttpResponseBadRequest.status_code, err_msg, None

    password = msg['password']
    email = msg['email']
    if msg['is_client']:
        client = authenticate(username=email, password=password,
                              is_client=msg['is_client'],
                              is_owner=msg['is_owner'])
        if not client:
            return 401, "Incorrect User/Password", None
        if client:
            return HttpResponse.status_code, '', client

    owner = authenticate(username=email, password=password,
                         is_client=msg['is_client'],
                         is_owner=msg['is_owner'])
    if not owner:
        return 401, "Incorrect User/Password",  None
    if owner:
        return HttpResponse.status_code, '', owner

    return HttpResponseServerError.status_code, "error authenticating user",\
        None
