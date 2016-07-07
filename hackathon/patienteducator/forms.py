from django import forms


class DateRangeField(forms.DateField):
    # to use with date range picker on appointments page

    def to_python(self, value):
        values = value.split(' - ')
        from_date = super(DateRangeField, self).to_python(values[0])
        to_date = super(DateRangeField, self).to_python(values[1])
        return from_date, to_date


class EducationalDocumentForm(forms.Form):
    docfile = forms.FileField(
        label='select a file',
        help_text='PDFs only'
    )


class DateRange(forms.Form):
    date_range = DateRangeField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': ('from'),
                   'class': 'form-control datepicker'}
        )
    )
