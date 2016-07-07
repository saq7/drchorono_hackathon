from django import forms


class EducationalDocumentForm(forms.Form):
    docfile = forms.FileField(
        label='select a file',
        help_text='PDFs only'
    )
