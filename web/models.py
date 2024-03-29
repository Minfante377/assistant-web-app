from datetime import timedelta
from random import randint

from utils.logger import logger

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class Client(models.Model):
    """
    This model defines the Client table.

    fields:
        - email(str):
        - password(str):
        - first_name(str):
        - last_name(str):
        - identity_number(int):

    """
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identity_number = models.IntegerField(unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name,
                                   self.identity_number)

    def save(self, *args, **kwargs):
        """
        This method hashes the password before saving it.
        """
        self.password = make_password(self.password)
        self.id = int("2{}".format(str(self.identity_number)))
        super().save(*args, **kwargs)


class Owner(models.Model):
    """
    This model defines the Owner table.

    fields:
        - owner_id(int): owner id.
        - email(str):
        - password(str)
        - clients(ManyToManyField): Clients associated with this owner.

    """
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField(null=True, blank=True)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identity_number = models.IntegerField(unique=True)
    clients = models.ManyToManyField(Client, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        This method initializes the owner_id with a 4 random digit integer
        and hashes the password before saving it.
        """
        self.id = int("1{}".format(str(self.identity_number)))
        self.password = make_password(self.password)
        self.owner_id = randint(1000, 9999)
        super().save(*args, **kwargs)

    def add_client(self, client):
        """
        This method adds a client to the owner

        Args:
            - client(Client)

        """
        logger.log_info("Adding client {}".format(client))
        self.clients.add(client)

    def delete_client(self, client_id_number):
        """
        This method removes a client by client identity number.

        Args:
            - client_id_number(int):

        Returns(None)

        """
        client = self.clients.all().filter(identity_number=client_id_number)
        if client:
            logger.log_info("Deleting client {}".format(client_id_number))
            self.clients.remove(client[0])
            return

        logger.log_error("Client {} not found. Unable to delete"
                         .format(client_id_number))


class Calendar(models.Model):
    """
    This model defines the Calendar table.

    fields:
        - summary(str): Calendar name.
        - owner(Owner): The owner the calendar belongs to.

    """
    summary = models.CharField(max_length=50)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} {}".format(self.owner.email, self.summary)

    def create_event(self, day, start_time, end_time, location,
                     recurrent=False):
        """
        Creates a new event on this calendar.

        Args:
            - day(date):
            - start_time(time):
            - end_time(time):
            - location(string):
            - recurrent(bool):

        Returns(None):

        """
        if end_time <= start_time:
            logger.log_error("End time must be greater than start time")
            raise ValidationError("End time must be greater than start time")

        events = Event.objects.filter(day=day, calendar=self)
        if events.exists():
            for event in events:
                if self._check_overlap(
                        event.start_time,
                        event.end_time,
                        start_time,
                        end_time):
                    logger.log_error("This event overlaps with another event")
                    raise ValidationError(
                        "This event overlaps with another event")

        Event.objects.create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            location=location,
            calendar=self)
        logger.log_info("New event added")
        if recurrent:
            logger.log_info("Creating recurrent event")
            end_date = day + timedelta(days=365)
            next_date = day + timedelta(days=7)
            while next_date < end_date:
                self.create_event(next_date, start_time, end_time, location)
                next_date += timedelta(days=7)

    def delete_event(self, day, start_time, end_time, all_events=False):
        """
        Delete an event.

        Args:
            - day(date):
            - start_time(time):
            - end_time(time):
            - all_events(bool):

        Returns(None):
        """
        logger.log_info("Deleting event {}:{}-{}".format(
                        day, start_time, end_time))

        if all_events:
            week_day = (day.weekday() + 1) % 7 + 1
            event = Event.objects.filter(
                calendar=self,
                start_time=start_time,
                end_time=end_time,
                day__week_day=week_day)
            event.delete()
            return
        Event.objects.filter(
            calendar=self, day=day,
            start_time=start_time,
            end_time=end_time).delete()

    def get_events(self, **kwargs):
        """
        Get events linked to this calendar and filter them by kwargs

        Args:

        Returns(list):
            list of Event instances.

        """
        logger.log_info("Getting event {}".format(kwargs))
        return Event.objects.filter(calendar=self, **kwargs)

    def assign_event(self, client_id_number, day, start_time, end_time):
        """
        Assign a free event to a client.

        Args:
            - day(date):
            - start_time(time):
            - end_time(time):
            - client_id_number(int):

        Returns(None):

        """
        logger.log_info("Assigning event {}:{}-{} to client {}"
                        .format(day, start_time, end_time, client_id_number))
        event = Event.objects.get(
            day=day,
            start_time=start_time,
            end_time=end_time,
            calendar=self)
        if not event.free:
            logger.log_error("Event is already taken")
            raise ValidationError("Event is already taken")

        client = Client.objects.get(identity_number=client_id_number)
        event.client = client
        event.free = False
        event.save()

    def free_event(self, day, start_time, end_time):
        """
        Free event.

        Args:
            - day(date):
            - start_time(time):
            - end_time(time):

        Returns(None):
        """
        logger.log_info("Freing Event {}:{}-{}"
                        .format(day, start_time, end_time))
        event = Event.objects.get(
            day=day,
            start_time=start_time,
            end_time=end_time,
            calendar=self)
        event.client = None
        event.free = True
        event.save()

    def _check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        """
        Check overlap between two events.

        Args:
            - fixed_start(time):
            - fixed_end(time):
            - new_start(time):
            - new_end(time):

        Returns(bool):
            True means overlap.

        """
        overlap = False

        if (new_start >= fixed_start and new_start <= fixed_end) or \
                (new_end >= fixed_start and new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap


class Event(models.Model):
    """
    This model defines the Event table.

    fields:
        - day(DateField):
        - start_time(TimeField):
        - end_time(TimeField):
        - location(str):
        - free(bool):
        - client(Client):
        - calendar(Calendar): The calendar the event belongs to.

    """
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=50, null=True)
    free = models.BooleanField(default=True)
    client = models.OneToOneField(Client, null=True,
                                  on_delete=models.DO_NOTHING)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} {} to {}".format(
            self.calendar.summary,
            self.day,
            self.start_time,
            self.end_time)
