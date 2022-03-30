import json

from .helpers import register_helper
from utils.error import error_map
from utils.logger import logger

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
    """
    This view redirects the user to the login page.
    """
    return redirect(reverse('login'))


@require_http_methods(['GET'])
def login(request):
    """
    This view defines the login page.
    """
    return render(request, 'login.html')


@require_http_methods(['GET'])
def register(request):
    """
    This view defines the register page
    """
    return render(request, 'register.html')


@require_http_methods(['POST'])
def register_user(request):
    """
    This view register a new Client or Owner

    Method: POST

    input:
        { "is_client": bool,
          "is_owner": bool,
          "email": str,
          "password": str,
          "first_name": optional[str],
          "last_name": optional[str],
          "identity_number": optional[str]
        }

    response: {'err_msg': str}

    """
    logger.log_info("/register_user/")
    content = json.loads(request.body.decode('utf-8'))
    logger.log_info("Trying to register user {}".format(content['email']))

    status_code, err_msg = register_helper.register_user(content)
    logger.log_info("Result: {}-{}".format(status_code, err_msg))

    if status_code != 200:
        user_err_msg = error_map(status_code)
        return HttpResponse(status=status_code, reason=user_err_msg)

    logger.log_info("Success registering user")
    return JsonResponse({})
