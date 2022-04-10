from .models import Client, Owner

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user using email/password.

        Args:
            - email(str):
            - password(str):

        Returns(Client/Owner):
        """
        if kwargs['is_client']:
            try:
                client = Client.objects.get(email=username)
                if client:
                    if check_password(password, client.password):
                        return client
            except Exception as e:
                print(e)
                return None

        if kwargs['is_owner']:
            try:
                owner = Owner.objects.get(email=username)
                if owner:
                    if check_password(password, owner.password):
                        return owner
            except Exception as e:
                print(e)
                return None
        return None

    def get_user(self, user_id):
        try:
            return Owner.objects.get(pk=user_id)
        except Owner.DoesNotExist:
            try:
                return Client.objects.get(pk=user_id)
            except Client.DoesNotExist:
                return None
