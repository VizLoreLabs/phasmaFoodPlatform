from django.conf import settings
from django.http import HttpRequest
from django.forms import Form
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def respond_email_verification_sent(self, request: HttpRequest, user: User) -> None:
        pass

    def send_confirmation_mail(self, request: HttpRequest, emailconfirmation: EmailConfirmation, signup: bool) -> None:
        current_site = get_current_site(request)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": emailconfirmation.key,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)

    def save_user(self, request: HttpRequest, user: User, form: Form, commit: bool = True) -> User:
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        super(AccountAdapter, self).save_user(request, user, form, commit=False)
        data = form.cleaned_data
        company = data.get("company", "")
        user_type = data.get("user_type", "")
        if commit:
            if company:
                user.company = company
            if user_type:
                user.user_type = user_type
            user.save()
        return user
