def is_client(model_object):
    """
    Defines whether the model_object is a client instance.

    Args:
        model_object(BaseModel):

    Return(bool):

    """
    try:
        model_object.identity_number
        return True
    except Exception:
        return False


def is_owner(model_object):
    """
    Defines whether the model_object is a client instance.

    Args:
        model_object(BaseModel):

    Return(bool):

    """
    try:
        model_object.owner_id
        return True
    except Exception:
        return False
