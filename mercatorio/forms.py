from django import forms
from .models import PersonalDocument

from .utils.validate_document import validate_document_extension, validate_file_size

class PersonalDocumentForm(forms.ModelForm):
    class Meta:
        model = PersonalDocument
        fields = ['doc_type', 'file']
        labels = {
            'doc_type': 'Tipo de Documento',
            'file': 'Documento',
        }
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'form-select w-25', 'requered': 'true'}),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }

    def clean_files(self):
        file = self.cleaned_data.get('file')

        validate_document_extension(file)
        validate_file_size(file)

        return file