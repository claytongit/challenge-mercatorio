from django.test import TestCase, override_settings
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from mercatorio.forms import PersonalDocumentForm, CertificateForms
from unittest.mock import patch

from mercatorio.models import Creditor, Certificate, Precatorio, PersonalDocument
from django.utils import timezone

import requests_mock

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

@patch('random.choice')
class APIMockTest(TestCase):
    def test_api_mock_return_certificate_fix(self, mock_choice):
        status = ['negative', 'positive', 'invalid', 'pending']
        tipos = ['federal', 'state', 'municipal', 'labor']
        mock_choice.side_effect = [val for pair in zip(status, tipos) for val in pair]

        response = self.client.get('/api/certidoes?cpf_cnpj=12345678900')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['cpf_cnpj'], '12345678900')
        self.assertEqual(len(data['certidoes']), 4)

        self.assertEqual(data['certidoes'][0]['tipo'], 'federal')
        self.assertEqual(data['certidoes'][0]['status'], 'negative')
        self.assertEqual(data['certidoes'][0]['file_url'], '/media/certificates/federal_fake_certidao.pdf')

class SearchCertificatesViewTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name='Teste User',
            cpf_cnpj='12345678900',
            email='teste@example.com',
            phone='11999999999'
        )

    def test_search_certificates_view_save_certificates(self):
        mock_response = {
            "cpf_cnpj": "12345678900",
            "certidoes": [
                {"tipo": "federal", "status": "negative", "file_url": "/media/certificates/federal_fake_certidao.pdf"},
                {"tipo": "labor", "status": "positive", "file_url": "/media/certificates/labor_fake_certidao.pdf"},
            ]
        }

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/api/certidoes', json=mock_response)

            response = self.client.post(f'/credores/{self.creditor.id}/buscar-certidoes')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Certificate.objects.filter(creditor=self.creditor).count(), 2)

            certs = Certificate.objects.filter(creditor=self.creditor)
            tipos = [c.cert_type for c in certs]
            self.assertIn('federal', tipos)
            self.assertIn('labor', tipos)

class CreditorDetailViewTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name='Maria Silva',
            cpf_cnpj='12345678900',
            email='maria@example.com',
            phone='11999999999'
        )

        self.precatorio = Precatorio.objects.create(
            creditor=self.creditor,
            precatorio_number='0001234-56.2020.8.26.0050',
            nominal_value=50000.0,
            forum='TJSP',
            publication_date='2023-10-01'
        )

        self.document = PersonalDocument.objects.create(
            creditor=self.creditor,
            doc_type='RG',
            file_url='/media/documents/rg_maria.pdf',
            submitted_at=timezone.now()
        )

        self.certificate = Certificate.objects.create(
            creditor=self.creditor,
            cert_type='federal',
            status='negative',
            origin='api',
            file_url='/media/certificates/federal_fake_certidao.pdf',
            received_at=timezone.now()
        )

    def test_credor_detail_endpoint_returns_complete_data(self):
        response = self.client.get(f'/credores/{self.creditor.id}')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Credor
        self.assertEqual(data['name'], 'Maria Silva')
        self.assertEqual(data['cpf_cnpj'], '12345678900')

        # Precatorio
        self.assertEqual(data['precatorio']['precatorio_number'], '0001234-56.2020.8.26.0050')

        # Documentos
        self.assertEqual(len(data['documents']), 1)
        self.assertEqual(data['documents'][0]['doc_type'], 'RG')
        self.assertEqual(data['documents'][0]['file_url'], '/media/documents/rg_maria.pdf')

        # Certidões
        self.assertEqual(len(data['certificates']), 1)
        self.assertEqual(data['certificates'][0]['cert_type'], 'federal')
        self.assertEqual(data['certificates'][0]['status'], 'negative')