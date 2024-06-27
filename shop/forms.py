# В файле forms.py вашего приложения или в том же файле, где находится ваш PaymentView
from django import forms
import re
from shop.models import Comment


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Номер карты', max_length=16)
    expiration_date = forms.CharField(label='Срок действия', max_length=5, help_text='Формат: MM/YY')
    cvv = forms.CharField(label='CVV', max_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        # Проверка формата номера карты с использованием регулярного выражения
        if not re.match(r'^\d{16}$', card_number):
            raise forms.ValidationError('Неверный формат номера карты. Введите 16 цифр.')
        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        # Проверка формата срока действия карты с использованием регулярного выражения
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiration_date):
            raise forms.ValidationError('Неверный формат срока действия карты. Используйте формат MM/YY.')
        return expiration_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        # Проверка формата CVV с использованием регулярного выражения
        if not re.match(r'^\d{3}$', cvv):
            raise forms.ValidationError('Неверный формат CVV. Введите 3 цифры.')
        return cvv


class DeliveryForm(forms.Form):
    city = forms.CharField(label='Город', max_length=100)
    address = forms.CharField(label='Адрес', max_length=255)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }