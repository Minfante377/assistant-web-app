from .models import Client, Owner

from django import forms


class ClientForm(forms.ModelForm):
    """
    This class implements the Client Form.
    """

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ('email', 'password', 'first_name', 'last_name',
                  'identity_number')


class OwnerForm(forms.ModelForm):
    """
    This class implements the Owner Form.
    """

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Owner
        fields = ('email', 'password')
