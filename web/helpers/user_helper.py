from ..models import Client


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
