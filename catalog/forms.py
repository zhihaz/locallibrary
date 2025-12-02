# catalog/forms.py
from django import forms
from catalog.models import BookInstance
import datetime

# Модельная форма для продления книги
class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': 'Дата продления'}
        help_texts = {'due_back': 'Введите дату между сегодня и 4 неделями вперед (по умолчанию 3 недели).'}

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Запретить дату в прошлом
        if data < datetime.date.today():
            raise forms.ValidationError('Неверная дата - дата уже прошла.')

        # Запретить дату больше чем через 4 недели
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError('Неверная дата - продление более чем на 4 недели.')

        return data

# Простая форма для продления книги без привязки к модели
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        label="Дата продления",
        help_text="Введите дату между сегодня и 4 неделями вперед."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise forms.ValidationError('Неверная дата - дата уже прошла.')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError('Неверная дата - продление более чем на 4 недели.')

        return data
