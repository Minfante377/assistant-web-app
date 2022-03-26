from random import randint

from utils.logger import logger

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
    password = models.CharField(max_length=20)
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
    password = models.CharField(max_length=20)
    clients = models.ManyToManyField(Client)

    def __init__(self, *args, **kwargs):
        """
        This method initializes the owner_id with a 4 random digit integer.
        """
        kwargs['owner_id'] = randint(1000, 9999)
        super().__init__(*args, **kwargs)

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
            self.clients.remove(client)
            return

        logger.log_error("Client {} not found. Unable to delete"
                         .format(client_id_number))
