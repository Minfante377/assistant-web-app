from web.models import Calendar, Client, Owner

from django.http import HttpResponseBadRequest, JsonResponse
from django.test import TestCase
from django.urls import reverse

TEST_EMAIL = 'test@test.com'
TEST_ID = '12345678'
TEST_PASSWORD = 'superSafePass'
TEST_FIRST_NAME = 'john'
TEST_LAST_NAME = 'doe'
TEST_SUMMARY = 'test'


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
        self.assertEqual(response.status_code, JsonResponse({}).status_code)
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
                'first_name': TEST_FIRST_NAME,
                'last_name': TEST_LAST_NAME,
                'identity_number': TEST_ID
                }
        response = self.client.post(
            reverse('register_user'),
            data=body,
            content_type='application/json')
        self.assertEqual(response.status_code, JsonResponse({}).status_code)
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
            response.status_code,
            HttpResponseBadRequest.status_code,
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
            response.status_code,
            HttpResponseBadRequest.status_code,
            msg='The request did not fail with both flags enabled')


class LoginUserViewTest(TestCase):
    """
    This class implements all the unit tests for the login_user view.
    """

    def setUp(self):
        """
        Create the test client and owner.
        """
        Client.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                              first_name=TEST_FIRST_NAME,
                              last_name=TEST_LAST_NAME,
                              identity_number=TEST_ID)
        Owner.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                             first_name=TEST_FIRST_NAME,
                             last_name=TEST_LAST_NAME,
                             identity_number=TEST_ID)

    def test_login_client(self):
        """
        This test logins a client.
        """
        body = {'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                'is_client': True,
                'is_owner': False}

        response = self.client.post(
            reverse('login_user'),
            data=body,
            content_type='application/json')

        self.assertEqual(response.status_code, JsonResponse({}).status_code)

    def test_login_owner(self):
        """
        This test logins an owner.
        """
        body = {'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                'is_client': False,
                'is_owner': True}

        response = self.client.post(
            reverse('login_user'),
            data=body,
            content_type='application/json')

        self.assertEqual(response.status_code, JsonResponse({}).status_code)

    def test_bad_request_no_flag(self):
        """
        This test tries to login a client or owner without is_client or
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
            response.status_code,
            HttpResponseBadRequest.status_code,
            msg='The request did not fail with no flags enabled')

    def test_bad_request_both_flags(self):
        """
        This test tries to login a client or owner with is_client and
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
            response.status_code,
            HttpResponseBadRequest.status_code,
            msg='The request did not fail with both flags enabled')


class AddOwnerClientViewTest(TestCase):
    """
    This class implements all the tests for the add_owner_client view.
    """

    def setUp(self):
        """
        Creates a client and owner.
        """
        self.user_client =\
            Client.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                                  first_name=TEST_FIRST_NAME,
                                  last_name=TEST_LAST_NAME,
                                  identity_number=TEST_ID)
        self.user_owner =\
            Owner.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                                 first_name=TEST_FIRST_NAME,
                                 last_name=TEST_LAST_NAME,
                                 identity_number=TEST_ID)

    def tearDown(self):
        """
        Delete test client and owner.
        """
        self.user_client.delete()
        self.user_owner.delete()
        self.client.logout()

    def test_add_owner_client(self):
        """
        This tests adds a new client to the owner's list.
        """
        self.client.force_login(
            self.user_owner)
        body = {'email': TEST_EMAIL,
                'identity_number': TEST_ID}
        self.client.post(
            reverse('add_owner_client'),
            body,
            content_type='application/json'
        )

        self.assertGreater(self.user_owner.clients.count(), 0,
                           msg='Client was not added to owners list')


class DeleteOwnerClientViewTest(TestCase):
    """
    This class implements all the tests for the delete_owner_client view.
    """

    def setUp(self):
        """
        Creates a client and owner.
        """
        self.user_client =\
            Client.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                                  first_name=TEST_FIRST_NAME,
                                  last_name=TEST_LAST_NAME,
                                  identity_number=TEST_ID)
        self.user_owner =\
            Owner.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                                 first_name=TEST_FIRST_NAME,
                                 last_name=TEST_LAST_NAME,
                                 identity_number=TEST_ID)

    def tearDown(self):
        """
        Delete test client and owner.
        """
        self.user_client.delete()
        self.user_owner.delete()
        self.client.logout()

    def test_delete_owner_client(self):
        """
        This test deletes a client from the owner's list.
        """
        self.client.force_login(
            self.user_owner)
        self.user_owner.clients.add(self.user_client)
        body = {'client_id': TEST_ID}
        self.client.post(
            reverse('delete_owner_client'),
            body,
            content_type='application/json'
        )

        self.assertEqual(self.user_owner.clients.count(), 0,
                         msg='Client was not deleted from owners list')


class AddOwnerCalendarViewTest(TestCase):
    """
    This class implements all the tests for the add_owner_calendar view.
    """

    def setUp(self):
        """
        Creates an owner.
        """
        self.user_owner =\
            Owner.objects.create(email=TEST_EMAIL, password=TEST_PASSWORD,
                                 first_name=TEST_FIRST_NAME,
                                 last_name=TEST_LAST_NAME,
                                 identity_number=TEST_ID)

    def tearDown(self):
        """
        Delete test owner.
        """
        self.user_owner.delete()
        self.client.logout()

    def test_add_owner_client(self):
        """
        This tests adds a new calendar to an owner.
        """
        self.client.force_login(
            self.user_owner)
        body = {'summary': TEST_SUMMARY}
        self.client.post(
            reverse('add_owner_calendar'),
            body,
            content_type='application/json'
        )

        calendar = Calendar.objects.get(owner=self.user_owner)

        self.assertEqual(calendar.summary, TEST_SUMMARY,
                         msg='Calendar was not bounded to owner')
