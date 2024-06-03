from django import forms
from .models import CallBackModel


class CallBackForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        return f'{name.upper()}'

    class Meta:
        model = CallBackModel
        fields = ('name', 'phone', 'date', 'time', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Ваше ім\'я',
                                           'data-rule': 'minlen:4'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш номер телефону',
                                            'id': 'email', 'data-rule': 'email'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM', 'type': 'time'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Додаткові побажання'}),
        }
        labels = {
            'name': 'Ім\'я',
            'phone': 'Телефон',
            'date': 'Дата',
            'time': 'Час',
            'comment': 'Додаткові побажання',
        }
        help_texts = {
            'phone': 'Введіть номер телефону у форматі +380XXXXXXXXX',
        }

