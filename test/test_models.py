import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from web.models import Calendar, Client, Event, Owner

TEST_ID_NUMBER = "12345678"
TEST_DAY = datetime.date.today()
TEST_START_TIME = datetime.time(00, 00, 00)
TEST_END_TIME = datetime.time(00, 30, 00)


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


class TestCalendar(TestCase):
    """
    This class implements all the unit tests for the Calendar Model Class
    """

    def setUp(self):
        """
        The setUp creates a test Calendar and a test Owner.
        """
        self.owner = Owner.objects.create(
            email="test@test.com",
            password="test")
        self.calendar = Calendar.objects.create(
            summary="test calendar",
            owner=self.owner)

    def tearDown(self):
        """
        The tearDown deletes the test Owner and test Calendar.
        """
        self.owner.delete()

    def test_create_event(self):
        """
        This test creates a new event.
        """
        self.calendar.create_event(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            location='test')

        self.assertEqual(Event.objects.filter(calendar=self.calendar).count(),
                         1, msg="Event was not created")

    def test_create_event_start_after_end(self):
        """
        This test creates a new event with start_time > end_tine and
        assert exception is raised
        """
        with self.assertRaises(ValidationError,
                               msg="start/end time error not detected"):
            self.calendar.create_event(
                day=TEST_DAY,
                start_time=TEST_END_TIME,
                end_time=TEST_START_TIME,
                location='test')

    def test_create_event_overlap(self):
        """
        Try to create an overlaping event. Assert exception is raised.
        """
        Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar)
        with self.assertRaises(ValidationError,
                               msg="Overlap was not detected"):
            self.calendar.create_event(
                day=TEST_DAY,
                start_time=TEST_START_TIME,
                end_time=TEST_END_TIME,
                location='test')
