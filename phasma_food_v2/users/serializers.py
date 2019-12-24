from typing import Any

from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.http import HttpRequest
from rest_framework import serializers, exceptions
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.utils.translation import ugettext_lazy as _

from .permissions import COMPANY, USER_TYPE

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs: dict) -> bool:
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email: dict, password: dict) -> Any:
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs: dict) -> Any:
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if allauth_settings.AUTHENTICATION_METHOD == allauth_settings.AuthenticationMethod.EMAIL:
            user = self._validate_email(email, password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class UserDetailsSerializer(serializers.ModelSerializer):
    """User detail serializer that is used in login
    serializer for user details.
    """

    class Meta:
        model = User
        fields = ("pk", "email", "first_name", "last_name", "company", "user_type")
        read_only_fields = ("email", "company", "user_type")


class UserRegisterSerializer(serializers.Serializer):
    """User registration serializer where project partners automatically
    are assigned a role of EXPERT user.
    """

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> Any:
        """Check user company and type

        Parameters:
            attrs (dict): User dictionary

        Returns:
            attrs (dict): User dictionary
        """
        email = attrs.get("email", "")
        password1 = attrs.get("password1", "")
        password2 = attrs.get("password2", "")
        if password1 != password2:
            raise serializers.ValidationError(_("The two password fields didn't match."))

        domain = email.split("@")[1]
        for k, v in COMPANY.items():
            if domain.lower() == v:
                attrs["company"] = k
                attrs["user_type"] = USER_TYPE.get("EXPERT", "")

        return attrs

    def validate_email(self, email: str) -> Any:
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password: str) -> str:
        return get_adapter().clean_password(password)

    def save(self, request: HttpRequest) -> User:
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user

    def get_cleaned_data(self) -> dict:
        """Data that is returned before save
        with company and user type added

        Returns:
            data (dict): Usr dictionary
        """
        data = {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "company": self.validated_data.get("company", ""),
            "user_type": self.validated_data.get("user_type", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }
        return data
