from consts import ErrorMap
from web.models import Client, Owner

from django.http import HttpResponse, HttpResponseBadRequest
from django.test import TestCase
from django.urls import reverse

TEST_EMAIL = 'test@test.com'
TEST_ID = '12345678'
TEST_PASSWORD = 'superSafePass'
TEST_FIRST_NAME = 'john'
TEST_LAST_NAME = 'doe'


class RegisterUserViewTest(TestCase):
    """
    This class implements all the unit tests for the register_user view.
    """

    def test_register_client(self):
        """
        This test registers a client.
        """
        body = {'is_client': True,
                'is_owner': False,
                'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                'first_name': TEST_FIRST_NAME,
                'last_name': TEST_LAST_NAME,
                'identity_number': TEST_ID
                }
        response = self.client.post(
            reverse('register_user'),
            data=body,
            content_type='application/json')
        self.assertEqual(
            response.context['err_msg'],
            ErrorMap.USER_ERRORS[str(HttpResponse.status_code)],
            msg='Error registering client')
        client = Client.objects.get(email=TEST_EMAIL, identity_number=TEST_ID)
        self.assertIsNotNone(client, msg='Client was not registered')

    def test_register_owner(self):
        """
        This test registers an owner.
        """
        body = {'is_client': False,
                'is_owner': True,
                'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                }
        response = self.client.post(
            reverse('register_user'),
            data=body,
            content_type='application/json')
        self.assertEqual(response.context['err_msg'], '',
                         msg='Error registering client')
        owner = Owner.objects.get(email=TEST_EMAIL)
        self.assertIsNotNone(owner, msg='Owner was not registered')

    def test_bad_request_no_flag(self):
        """
        This test tries to register a client or owner without is_client or
        is_owner set.
        """
        body = {'email': TEST_EMAIL,
                'is_client': False,
                'is_owner': False,
                }
        response = self.client.post(
            reverse('register_user'),
            data=body,
            content_type='application/json')
        self.assertEqual(
            response.context['err_msg'],
            ErrorMap.USER_ERRORS[str(HttpResponseBadRequest.status_code)],
            msg='The request did not fail with no flags enabled')

    def test_bad_request_both_flags(self):
        """
        This test tries to register a client or owner with is_client and
        is_owner set.
        """
        body = {'email': TEST_EMAIL,
                'is_client': True,
                'is_owner': True,
                }
        response = self.client.post(
            reverse('register_user'),
            data=body,
            content_type='application/json')
        self.assertEqual(
            response.context['err_msg'],
            ErrorMap.USER_ERRORS[str(HttpResponseBadRequest.status_code)],
            msg='The request did not fail with both flags enabled')
