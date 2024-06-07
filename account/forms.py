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
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім`я користувача'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище користувача'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мобільний номер'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        labels = {
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'username': 'Мобільний номер',
            'email': 'Електронна пошта',
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
