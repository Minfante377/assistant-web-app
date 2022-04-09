import json

from .helpers import login_helper, register_helper, user_helper
from utils.error import error_map
from utils.logger import logger

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
    """
    This view redirects the user to the login page.
    """
    return redirect(reverse('login'))


@require_http_methods(['GET'])
def login_view(request):
    """
    This view defines the login page.
    """
    return render(request, 'login.html')


@require_http_methods(['GET'])
def register_view(request):
    """
    This view defines the register page
    """
    return render(request, 'register.html')


@login_required(login_url="/login")
@require_http_methods(['GET'])
def owner_view(request):
    """
    This view defines the owner page.
    """
    if user_helper.is_client(request.user):
        return redirect(reverse("client_view"))
    return render(request, "owner.html")


@login_required(login_url="/login")
@require_http_methods(['GET'])
def client_view(request):
    """
    This view defines the client page.
    """
    if user_helper.is_owner(request.user):
        return redirect(reverse("owner_view"))
    return render(request, "client.html")


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


@require_http_methods(['POST'])
def login_user(request):
    """
    This view logins an existing Client or Owner.

    Method: POST

    input:
        { "is_client": bool,
          "is_owner": bool,
          "email": str,
          "password": str,
        }

    response: {'err_msg': str}

    """
    logger.log_info("/login_user/")
    content = json.loads(request.body.decode('utf-8'))

    status_code, err_msg, user = login_helper.login_user(content)
    logger.log_info("Result: {} - {}".format(status_code, err_msg))

    if status_code != 200:
        user_err_msg = error_map(status_code)
        return HttpResponse(status=status_code, reason=user_err_msg)

    logger.log_info("Success loging in user")
    login(request, user)
    return JsonResponse({})
