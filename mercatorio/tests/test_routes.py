from django.test import TestCase, override_settings
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from mercatorio.forms import PersonalDocumentForm, CertificateForms
# from django.core.exceptions import ValidationError 

from mercatorio.models import Creditor

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

class CreateCreditorRouteTest(TestCase):
    def test_create_creditor_route(self):
        data = {
            "name": "Maria Silva",
            "cpf_cnpj": "12345678900",
            "email": "maria@example.com",
            "phone": "11999999999",
            "precatorio": {
                "precatorio_number": "0001234-56.2020.8.26.0050",
                "nominal_value": 50000.0,
                "forum": "TJSP",
                "publication_date": "2023-10-01"
            }
        }
        response = self.client.post('/credores', data, content_type='application/json')

        self.assertEqual(response.status_code, 201)
    
    def test_create_creditor_route_invalid_data(self):
        data = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "phone": "11999999999",
            "precatorio": {
                "precatorio_number": "0001234-56.2020.8.26.0050",
                "nominal_value": 50000.0,
                "forum": "TJSP",
                "publication_date": "2023-10-01"
            }
        }
        response = self.client.post('/credores', data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UploadDocumentRouteTest(TestCase):
    def setUp(self):
        self.form = PersonalDocumentForm
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )
    
    def create_temp_file(self, name='test.pdf', size=1024, content_type='application/pdf'):
        file = tempfile.NamedTemporaryFile(suffix='test.pdf')
        file.write(b'a' * size)
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type=content_type)

    def test_upload_document_route_view(self):
        response = self.client.get(f'/credores/{self.creditor.id}/documentos')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mercatorio/index.html')

    def test_upload_document_route_view_has_form(self):
        response = self.client.get(f'/credores/{self.creditor.id}/documentos')

        self.assertContains(response, '<form')
    
    def test_form_can_be_validated_pdf(self):
        file = self.create_temp_file(name='valid.pdf')
        form = self.form(
            data={'doc_type': 'RG'},
            files={'file': file}
        )

        self.assertTrue(form.is_valid())
    
    def test_form_can_be_invalidated_size(self):
        file = self.create_temp_file(name='large.pdf', size=10 * 1024 * 1024)
        form = self.form(
            data={'doc_type': 'RG'},
            files={'file': file}
        )

        self.assertFalse(form.is_valid())
    
    def test_form_can_be_invalidated_extension(self):
        file = self.create_temp_file(name='invalid.exe')
        form = self.form(
            data={'doc_type': 'RG'},
            files={'file': file}
        )

        self.assertFalse(form.is_valid())

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UploadCertificateRouteTest(TestCase):
    def setUp(self):
        self.form = CertificateForms
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )
    
    def create_temp_file(self, name='test.pdf', size=1024, content_type='application/pdf'):
        file = tempfile.NamedTemporaryFile(suffix='test.pdf')
        file.write(b'a' * size)
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type=content_type)

    def test_upload_certificate_route_view(self):
        response = self.client.get(f'/credores/{self.creditor.id}/certidoes')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mercatorio/certificate.html')

    def test_upload_certificate_route_view_has_form(self):
        response = self.client.get(f'/credores/{self.creditor.id}/certidoes')

        self.assertContains(response, '<form')
    
    def test_form_can_be_validated_pdf(self):
        file = self.create_temp_file(name='valid.pdf')
        form = self.form(
            data={'cert_type': 'federal', 'origin': 'manual', 'status': 'pending'},
            files={'file': file}
        )

        self.assertTrue(form.is_valid())
    
    def test_form_can_be_invalidated_size(self):
        file = self.create_temp_file(name='large.pdf', size=10 * 1024 * 1024)
        form = self.form(
            data={'cert_type': 'federal', 'origin': 'manual', 'status': 'pending'},
            files={'file': file}
        )

        self.assertFalse(form.is_valid())
    
    def test_form_can_be_invalidated_extension(self):
        file = self.create_temp_file(name='invalid.exe')
        form = self.form(
            data={'cert_type': 'federal', 'origin': 'manual', 'status': 'pending'},
            files={'file': file}
        )

        self.assertFalse(form.is_valid())