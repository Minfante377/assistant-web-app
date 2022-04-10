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
