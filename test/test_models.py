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
            first_name="test",
            last_name="test",
            identity_number=TEST_ID_NUMBER,
            password="test",)

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
        The setUp creates a test Calendar, a test Owner and a test Client.
        """
        self.owner = Owner.objects.create(
            email="test@test.com",
            password="test",
            first_name="test",
            last_name="test",
            identity_number=TEST_ID_NUMBER)
        self.calendar = Calendar.objects.create(
            summary="test calendar",
            owner=self.owner)
        self.client = Client.objects.create(
            email="test@test.com",
            password="testPass",
            first_name="test",
            last_name="test",
            identity_number=TEST_ID_NUMBER)

    def tearDown(self):
        """
        The tearDown deletes the test Owner and test Calendar.
        """
        self.owner.delete()
        self.client.delete()

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

    def test_delete_event(self):
        """
        This test deletes an event.
        """
        Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar)

        self.calendar.delete_event(day=TEST_DAY, start_time=TEST_START_TIME,
                                   end_time=TEST_END_TIME)
        self.assertEqual(Event.objects.filter(calendar=self.calendar).count(),
                         0, msg='Failed to delete event')

    def test_get_events(self):
        """
        This test get the events from the test Calendar.
        """
        event = Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar)

        self.assertEqual(
            event,
            self.calendar.get_events(day=TEST_DAY)[0],
            msg='Events werent fetched correctly')

    def test_assign_event(self):
        """
        This test assigns a test Event to the test Client.
        """
        event = Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar)
        self.calendar.assign_event(self.client.identity_number, event.day,
                                   event.start_time, event.end_time)
        self.assertEqual(event, Event.objects.get(client=self.client),
                         msg="Event was not assigned")

    def test_assign_event_already_assigned(self):
        """
        This test assigns a test Client to an already assigned event and
        asserts an exception is raised.
        """
        event = Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar,
            free=False)
        with self.assertRaises(ValidationError,
                               msg='An event cannot be assigned twice'):
            self.calendar.assign_event(self.client.identity_number, event.day,
                                       event.start_time, event.end_time)

    def test_free_event(self):
        """
        This test frees an event.
        """
        event = Event.objects.create(
            day=TEST_DAY,
            start_time=TEST_START_TIME,
            end_time=TEST_END_TIME,
            calendar=self.calendar,
            free=False,
            client=self.client)
        self.calendar.free_event(day=event.day, start_time=event.start_time,
                                 end_time=event.end_time)
        msg = 'Event was not freed correctly'
        event.refresh_from_db()
        self.assertEqual(event.free, True, msg=msg)
        self.assertEqual(event.client, None, msg=msg)
