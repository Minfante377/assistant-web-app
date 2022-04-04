from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseServerError


class ErrorMap:
    USER_ERRORS = {
        str(HttpResponse.status_code): '',
        str(HttpResponseBadRequest.status_code):
            'Hubo un error con su '
            'solicitud. Por favor revisela e intentelo nuevamente.',
            str(HttpResponseServerError.status_code):
                'Hubo un error al '
                'procesar su solicitud. Intentelo nuevamente mas tarde.',
        '401': 'Usuario o Contraseña incorrecto.'
    }
