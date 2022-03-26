from django.test import TestCase

from web.models import Client, Owner

TEST_ID_NUMBER = "12345678"


class TestClient(TestCase):
    """
    This class implements all the unit tests for the Client Model Class
    """
    pass


class TestOwner(TestCase):
    """
    This class implements all the unit tests for the Owner Model Class
    """

    def setUp(self):
        """
        The setUp creates a test Owner and a test Client.
        """
        self.client = Client.objects.create(
            email="test@test.com",
            password="testPass",
            first_name="test",
            last_name="test",
            identity_number=TEST_ID_NUMBER)
        self.owner = Owner.objects.create(
            email="test@test.com",
            password="test")

    def tearDown(self):
        """
        The tearDown deletes the test Owner and test Client.
        """
        self.client.delete()
        self.owner.delete()

    def test_add_client(self):
        """
        This test adds the test client to the test owner
        """
        self.owner.add_client(self.client)
        self.assertGreater(self.owner.clients.count(), 0,
                           msg="Client was not added")

    def test_delete_client(self):
        """
        This test delete the test client from the test owner using the client
        identity number
        """
        self.owner.delete_client(TEST_ID_NUMBER)
        self.assertEqual(self.owner.clients.count(), 0,
                         msg="Client was not deleted")
