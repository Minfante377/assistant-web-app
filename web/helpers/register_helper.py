from ..models import Client, Owner

from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseServerError


def register_user(msg):
    """
    This function register a new Client or Owner.

    Args:
        - msg(dict): {
            "is_client": bool,
            "is_owner": bool,
            "email": str,
            "password": str,
            "first_name": optional[str],
            "last_name": optional[str],
            "identity_number": optional[str]
          }

    Returns(tupple):
    (status_code, err_msg)

    """
    if msg['is_client'] and msg['is_owner']:
        err_msg = "Only one of the fields 'is_client' or 'is_owner' can be"\
            "set"
        return HttpResponseBadRequest.status_code, err_msg

    if not msg['is_client'] and not msg['is_owner']:
        err_msg = "One of the fields 'is_client' or 'is_owner' should be set"
        return HttpResponseBadRequest.status_code, err_msg

    if msg['is_client']:
        try:
            Client.objects.create(
                email=msg['email'],
                password=msg['password'],
                first_name=msg['first_name'],
                last_name=msg['last_name'],
                identity_number=msg['identity_number']
            )
            return HttpResponse.status_code, ''
        except Exception as e:
            return HttpResponseServerError.status_code, str(e)

    try:
        Owner.objects.create(
            email=msg['email'],
            password=msg['password']
        )
        return HttpResponse.status_code, ''
    except Exception as e:
        return HttpResponseServerError.status_code, str(e)
