import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):
    """
    Form for user registration.

    Includes fields for first name, last name, username (phone number), email,
    and password (with confirmation).

    Provides validation for username (phone number format) and password match.

    Attributes:
        password1 (forms.CharField): Password input field.
        password2 (forms.CharField): Confirm password input field.
    """

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Пароль')}),
        label=_('Пароль')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Підтвердження паролю')}),
        label=_('Підтвердження паролю')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ім`я користувача')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Прізвище користувача')}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Мобільний номер')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
        }
        labels = {
            'first_name': _('Ім`я'),
            'last_name': _('Прізвище'),
            'username': _('Мобільний номер'),
            'email': _('Електронна пошта'),
        }
        help_texts = {
            'first_name': _('Обов`язкове поле'),
            'last_name': _('Обов`язкове поле'),
            'username': _('Обов`язкове поле'),
            'email': _('Обов`язкове поле'),
        }
        error_messages = {
            'first_name': {
                'required': _('Обов`язкове поле'),
            },
            'last_name': {
                'required': _('Обов`язкове поле'),
            },
            'username': {
                'required': _('Обов`язкове поле'),
            },
            'email': {
                'required': _('Обов`язкове поле'),
            }
        }

    def clean_username(self):
        """
        Validate and format the username (phone number).

        Returns:
            str: Validated and formatted username.

        Raises:
            ValidationError: If the username does not match the required format.
        """
        username = self.cleaned_data['username']

        username = username.replace(' ', '')
        if not re.match(r'^(\+?380|0)\d{9}$', username):
            raise ValidationError(_('Невірний формат номеру телефону.'))
        if username.startswith('+380'):
            username = '0' + username[4:]
        elif username.startswith('380'):
            username = '0' + username[3:]
        return username

    def clean_password2(self):
        """
        Validate password confirmation.

        Returns:
            str: Confirmed password.

        Raises:
            forms.ValidationError: If passwords do not match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Паролі не співпадають'))
        return password2

    def save(self, commit=True):
        """
        Save user object with hashed password.

        Args:
            commit (bool, optional): Whether to save to the database. Defaults to True.

        Returns:
            User: Saved user object.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Form for user login.

    Includes fields for username (phone number) and password.

    Attributes:
        username (forms.CharField): Username (phone number) input field.
        password (forms.CharField): Password input field.
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Номер телефону')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Пароль')})
    )
