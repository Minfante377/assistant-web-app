import json

from .helpers import login_helper, register_helper, user_helper
from utils.error import error_map
from utils.logger import logger

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
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
    calendar = user_helper.get_owner_calendar(request.user)
    return render(request, "owner.html",
                  context={'owner': True, 'calendar': calendar})


@login_required(login_url="/login")
@require_http_methods(['GET'])
def owner_clients_view(request):
    """
    This view defines the owner clients list page.
    """
    if user_helper.is_client(request.user):
        return redirect(reverse("client_view"))
    clients = request.user.clients.all()
    return render(request, "clients_list.html",
                  context={'owner': True, 'clients': clients})


@login_required(login_url="/login")
@require_http_methods(['POST'])
def add_owner_client(request):
    """
    Add one client to the owners clients list.

    input:
        {'email': str,
         'identity_number': int
        }

    response: {'reason': err_msg }
    """
    if user_helper.is_client(request.user):
        return redirect(reverse("client_view"))
    content = json.loads(request.body.decode('utf-8'))
    logger.log_info("Trying to add client {}".format(content['email']))
    try:
        client = user_helper.get_client(
            email=content['email'],
            identity_number=content['identity_number'])
        request.user.add_client(client)
        return JsonResponse({})
    except Exception as err:
        logger.log_error("Error Adding client: {}".format(err))
        return HttpResponseBadRequest(reason=err)


@login_required(login_url="/login")
@require_http_methods(['POST'])
def delete_owner_client(request):
    """
    Delete one client from owners clients list.

    input:
        {'client_id': str}

    response: {'reason': err_msg}

    """
    if user_helper.is_client(request.user):
        return redirect(reverse("client_view"))
    content = json.loads(request.body.decode('utf-8'))
    logger.log_info("Trying to delete client {}".format(content['client_id']))
    try:
        request.user.delete_client(content['client_id'])
        return JsonResponse({})
    except Exception as err:
        logger.log_error("Error deleting client: {}".format(err))
        return HttpResponseBadRequest(reason=err)


@login_required(login_url="/login")
@require_http_methods(['POST'])
def add_owner_calendar(request):
    """
    Add a calendar to the owner.

    input:
        { 'summary': str}

    response: {'reason': err_msg}

    """
    if user_helper.is_client(request.user):
        return redirect(reverse("client_view"))
    content = json.loads(request.body.decode('utf-8'))
    logger.log_info("Trying to add calendar {}".format(content['summary']))
    try:
        user_helper.add_owner_calendar(request.user, content['summary'])
        return JsonResponse({})
    except Exception as err:
        logger.log_error("Error adding calendar: {}".format(err))
        return HttpResponseBadRequest(reason=err)


@login_required(login_url="/login")
@require_http_methods(['GET'])
def client_view(request):
    """
    This view defines the client page.
    """
    if user_helper.is_owner(request.user):
        return redirect(reverse("owner_view"))
    return render(request, "client.html", context={'client': True})


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
    if user_helper.is_client(user):
        return JsonResponse({"is_client": True})
    return JsonResponse({"is_client": False})


@login_required(login_url="/login")
@require_http_methods(['GET'])
def logout_user(request):
    """
    This view logouts an existing Client or Owner.
    """
    logout(request)
    return redirect(reverse("login"))
