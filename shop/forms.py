import re
from django import forms
from shop.models import Comment


class PaymentForm(forms.Form):
    """
    Form for handling payment details.
    """
    card_number = forms.CharField(label='Номер карты', max_length=16)
    expiration_date = forms.CharField(label='Срок действия', max_length=5, help_text='Формат: MM/YY')
    cvv = forms.CharField(label='CVV', max_length=3)

    def clean_card_number(self):
        """
        Validates the card number format.
        """
        card_number = self.cleaned_data['card_number']
        if not re.match(r'^\d{16}$', card_number):
            raise forms.ValidationError('Неверный формат номера карты. Введите 16 цифр.')
        return card_number

    def clean_expiration_date(self):
        """
        Validates the expiration date format.
        """
        expiration_date = self.cleaned_data['expiration_date']
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiration_date):
            raise forms.ValidationError('Неверный формат срока действия карты. Используйте формат MM/YY.')
        return expiration_date

    def clean_cvv(self):
        """
        Validates the CVV format.
        """
        cvv = self.cleaned_data['cvv']
        if not re.match(r'^\d{3}$', cvv):
            raise forms.ValidationError('Неверный формат CVV. Введите 3 цифры.')
        return cvv


class DeliveryForm(forms.Form):
    """
    Form for handling delivery details.
    """
    city = forms.CharField(label='Город', max_length=100)
    address = forms.CharField(label='Адрес', max_length=255)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    """
    Form for handling comments.
    """
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }
