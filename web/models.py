from random import randint

from django.db import models


class Client(models.Model):
    """
    This model defines the Client table.

    fields:
        - email(str):
        - first_name(str):
        - last_name(str):
        - identity_number(int):

    """
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=20, null=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identity_number = models.IntegerField(unique=True)


class Owner(models.Model):
    """
    This model defines the Owner table.

    fields:
        - owner_id(int): owner id.
        - email(str):
        - password(str)
        - clients(ManyToManyField): Clients associated with this owner.

    """
    owner_id = models.IntegerField()
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=20, null=False)
    clients = models.ManyToManyField(Client)

    def __init__(self, *args, **kwargs):
        """
        This method initializes the owner_id with a 4 random digit integer.
        """
        self.owner_id = randint.random(1000, 9999)
        super().__init__(*args, **kwargs)
