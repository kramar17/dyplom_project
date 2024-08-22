from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CallBackModel


class CallBackForm(forms.ModelForm):
    """
    Form for CallBackModel.

    Attributes:
        clean_name (method): Custom cleaning method for the 'name' field.
    """

    def clean_name(self):
        """
        Clean 'name' field to convert it to uppercase.

        Returns:
            str: Cleaned uppercase name.
        """
        name = self.cleaned_data['name']
        return f'{name.upper()}'

    class Meta:
        model = CallBackModel
        fields = ('name', 'phone', 'date', 'time', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': _('Ваше ім\'я'),
                                           'data-rule': 'minlen:4'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ваш номер телефону'),
                                            'id': 'phone', 'data-rule': 'phone'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': _('YYYY-MM-DD'), 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': _('HH:MM'), 'type': 'time'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Додаткові побажання')}),
        }
        labels = {
            'name': _('Ім\'я'),
            'phone': _('Телефон'),
            'date': _('Дата'),
            'time': _('Час'),
            'comment': _('Додаткові побажання'),
        }
        help_texts = {
            'phone': _('Введіть номер телефону у форматі +380XXXXXXXXX'),
        }
