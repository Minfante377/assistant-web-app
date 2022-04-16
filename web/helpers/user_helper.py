import datetime

from ..consts import Language
from ..models import Client, Calendar


def is_client(model_object):
    """
    Defines whether the model_object is a client instance.

    Args:
        model_object(BaseModel):

    Return(bool):

    """
    try:
        model_object.owner_id
        return False
    except Exception:
        return True


def is_owner(model_object):
    """
    Defines whether the model_object is an owner instance.

    Args:
        model_object(BaseModel):

    Return(bool):

    """
    try:
        model_object.owner_id
        return True
    except Exception:
        return False


def get_client(**kwargs):
    """
    Get a client based on certain filters.

    Args:

    Returns(Client):
    """
    return Client.objects.get(**kwargs)


def get_owner_calendar(owner):
    """
    Get the calendar bounded to an owner.

    Args:
        - owner(Owner)

    Returns(Calendar|None):
    """
    try:
        return Calendar.objects.get(owner=owner)
    except Exception:
        return None


def add_owner_calendar(owner, summary):
    """
    Add calendar to a certain owner.

    Args:
        - owner(Owner):
        - summarty(str):

    Returns(None):
    """
    calendar = Calendar.objects.create(summary=summary)
    calendar.owner = owner
    calendar.save()


def get_owner_events(owner, **kwargs):
    """
    Get all the owner's events for a certain month.

    Args:
        - owner(Owner):

    Returns(list): list of events

    """
    month = kwargs.get("month_filter")
    year = kwargs.get("year_filter")
    calendar = get_owner_calendar(owner)
    events = calendar.get_events()
    if month and year:
        kwargs.pop('month_filter')
        kwargs.pop('year_filter')
        month =\
            Language.MONTH.get(month) if Language.MONTH.get(month) else month
        if isinstance(month, str):
            month = datetime.datetime.strptime(month, "%B").month
        events = events.filter(day__year=year, day__month=month, **kwargs)
    return events
