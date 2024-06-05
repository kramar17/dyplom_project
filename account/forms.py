import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім`я користувача'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище користувача'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мобільний номер'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
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

        username = username.replace(' ', '')
        if not re.match(r'^(\+?380|0)\d{9}$', username):
            raise ValidationError('Невірний формат номеру телефону.')
        if username.startswith('+380'):
            username = '0' + username[4:]
        elif username.startswith('380'):
            username = '0' + username[3:]
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефону'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

