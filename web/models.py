from django.db import models


class Client(models.Model):
    """
    This model defines the Client table.

    fields:
        - email(str): This field must be unique
        - first_name(str):
        - last_name(str):
        - identity_number(int): This field must be unique
        - approved(bool): Profile approved by owner or not.

    """
    email = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identity_number = models.IntegerField(unique=True)
    approved = models.BooleanField()
