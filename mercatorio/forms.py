from django import forms
from .models import PersonalDocument, Certificate

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
            'doc_type': forms.Select(attrs={'class': 'form-select', 'requered': 'true'}),
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

class CertificateForms(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['cert_type','origin','status','file']
        labels = {
            'cert_type': 'Tipo de Certificado',
            'origin': 'Origen',
            'status': 'Estado',
            'file': 'Certificado',
        }
        widgets = {
            'cert_type': forms.Select(attrs={'class': 'form-select', 'requered': 'true'}),
            'origin': forms.Select(attrs={'class': 'form-select', 'requered': 'true'}),
            'status': forms.Select(attrs={'class': 'form-select', 'requered': 'true'}),
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