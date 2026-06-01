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

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.room = room

        if room is not None:
            self.fields['guests'].max_value = room.capacity

            self.fields['guests'].widget.attrs.update({
                'max': room.capacity,
                'min': 1
            })