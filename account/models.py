import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}),
        label='Підтвердження паролю'
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім`я користувача'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище користувача'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мобільний номер'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

        labels = {
            'first_name': 'Ваше ім`я',
            'last_name': 'Ваше прізвище',
            'username': 'Ваш мобільний номер',
            'email': 'Ваш Email',
        }
        help_texts = {
            'first_name': 'Обов`язкове поле',
            'last_name': 'Обов`язкове поле',
            'username': 'Обов`язкове поле',
            'email': 'Обов`язкове поле',
        }
        error_messages = {
            'first_name': {
                'required': 'Обов`язкове поле',
            },
            'last_name': {
                'required': 'Обов`язкове поле',
            },
            'username': {
                'required': 'Обов`язкове поле',
            },
            'email': {
                'required': 'Обов`язкове поле',
            }
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^(\+?380|0)\d{9}$', username):
            raise ValidationError('Неверный формат номера телефона.')
        if username.startswith('+380'):
            username = '0' + username[4:]
        elif username.startswith('380'):
            username = '0' + username[3:]
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.capitalize()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit and self.is_valid():
            user.save()
        return user
