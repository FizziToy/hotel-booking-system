from django import forms


class BookingForm(forms.Form):
    check_in = forms.DateField(
        label='Дата заїзду',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    check_out = forms.DateField(
        label='Дата виїзду',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    guests = forms.IntegerField(
        label='Кількість гостей',
        min_value=1
    )