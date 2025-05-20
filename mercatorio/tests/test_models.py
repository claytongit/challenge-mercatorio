from django.test import TestCase, override_settings
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

from mercatorio.models import Creditor, Precatorio, PersonalDocument, Certificate

TEMP_MEDIA_ROOT = tempfile.mkdtemp()
# Create your tests here.
class CreditorTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )

    def test_creditor_creation(self):
        self.assertEqual(self.creditor.name, "Test Creditor")
        self.assertEqual(self.creditor.cpf_cnpj, "123.456.789-00")
        self.assertEqual(self.creditor.email, "test@example.com")
        self.assertEqual(self.creditor.phone, "(11) 9999-9999")
        self.assertEqual(str(self.creditor), "Test Creditor (123.456.789-00)")
    
    def test_creditor_creation_invalid_unique_cpf_cnpj(self):
        with self.assertRaises(IntegrityError):
            Creditor.objects.create(
                name="Duplicate Creditor",
                cpf_cnpj="123.456.789-00",  # Same CPF/CNPJ
                email="duplicate@example.com",
                phone="(11) 8888-8888"
            )

class PrecatorioTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )
        self.precatorio = Precatorio.objects.create(
            precatorio_number = "0001234-56.2020.8.26.0050",
            nominal_value = 50000.00,
            forum = "TJSP",
            publication_date = "2023-10-01",
            creditor = self.creditor
        )

    def test_precatorio_creation(self):
        self.assertEqual(self.precatorio.precatorio_number, "0001234-56.2020.8.26.0050")
        self.assertEqual(self.precatorio.nominal_value, 50000.00)
        self.assertEqual(self.precatorio.forum, "TJSP")
        self.assertEqual(self.precatorio.publication_date, "2023-10-01")
        self.assertEqual(self.precatorio.creditor, self.creditor)
        self.assertEqual(str(self.precatorio), "Precatório 0001234-56.2020.8.26.0050 - Test Creditor")
    
    def test_precatorio_creation_invalid_unique_precatorio_number(self):
        with self.assertRaises(IntegrityError):
            Precatorio.objects.create(
                precatorio_number = "0001234-56.2020.8.26.0050",  # Same precatorio_number
                nominal_value = 60000.00,
                forum = "TJSP",
                publication_date = "2023-10-02",
                creditor = self.creditor
            )
    
    def test_precatorio_creation_invalid_creditor_null(self):
        with self.assertRaises(IntegrityError):
            Precatorio.objects.create(
                precatorio_number = "0001234-56.2020.8.26.0051",
                nominal_value = 60000.00,
                forum = "TJSP",
                publication_date = "2023-10-02",
                creditor = None # Creditor Null
            )
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PersonalDocumentTest(TestCase):
    def setUp(self):
        file = self.create_temp_file(name='valid_doc.pdf')
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )
        self.personal_document = PersonalDocument.objects.create(
            doc_type = "RG",
            file = file,
            file_url = "media/documents/valid_doc.pdf",
            creditor = self.creditor
        )
    
    def create_temp_file(self, name='test.pdf', size=1024, content_type='application/pdf'):
        file = tempfile.NamedTemporaryFile(suffix='test.pdf')
        file.write(b'a' * size)
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type=content_type)

    def test_personal_document_creation(self):
        self.assertEqual(self.personal_document.doc_type, "RG")
        self.assertEqual(self.personal_document.file_url, "media/documents/valid_doc.pdf")
        self.assertEqual(str(self.personal_document), "RG - Test Creditor")
    
    def test_personal_document_creation_invalid_creditor_null(self):
        with self.assertRaises(IntegrityError):
            PersonalDocument.objects.create(
                doc_type = "RG",
                file_url = "media/documents/valid_doc.pdf",
                creditor = None # Creditor Null
            )

    def test_personal_document_creation_invalid_doc_type(self):
        personal_document = PersonalDocument.objects.create(
            doc_type = "PIS", # Invalid doc_type
            file_url = "media/documents/valid_doc.pdf",
            creditor = self.creditor
        )          

        with self.assertRaises(ValidationError):
            personal_document.full_clean()
    
    def test_invalid_file_size(self):
        file = self.create_temp_file(name='large.pdf', size=6 * 1024 * 1024)  # 6MB
        doc = PersonalDocument.objects.create(
            doc_type = "RG",
            file = file,
            file_url = "media/documents/valid_doc.pdf",
            creditor = self.creditor
        )
        with self.assertRaises(ValidationError) as context:
            doc.full_clean()
        self.assertIn('O arquivo é muito grande', str(context.exception))
    
    def test_invalid_extension(self):
        file = self.create_temp_file(name='invalid.exe')
        doc = PersonalDocument.objects.create(
            doc_type = "RG",
            file = file,
            file_url = "media/documents/valid_doc.pdf",
            creditor = self.creditor
        )
        with self.assertRaises(ValidationError) as context:
            doc.full_clean()
        self.assertIn('Extensão não permitida', str(context.exception))
        
class CertificateTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name="Test Creditor",
            cpf_cnpj="123.456.789-00",
            email="test@example.com",
            phone="(11) 9999-9999"
        )
        self.certificate = Certificate.objects.create(
            cert_type = "state",
            origin = "manual",
            file_url = "media/documents/valid_doc.pdf",
            status = "pending",
            creditor = self.creditor
        )
    def test_certificate_creation(self):
        self.assertEqual(self.certificate.cert_type, "state")
        self.assertEqual(self.certificate.origin, "manual")
        self.assertEqual(self.certificate.file_url, "media/documents/valid_doc.pdf")
        self.assertEqual(self.certificate.status, "pending")
        self.assertEqual(self.certificate.creditor, self.creditor)
        self.assertEqual(str(self.certificate), "state - Test Creditor (pending)")
    
    def test_certificate_creation_invalid_creditor_null(self):
        with self.assertRaises(IntegrityError):
            Certificate.objects.create(
                cert_type = "state",
                origin = "manual",
                file_url = "media/documents/valid_doc.pdf",
                status = "pending",
                creditor = None # Creditor Null
            )

    def test_certificate_creation_invalid_cert_type(self):
        certificate = Certificate.objects.create(
            cert_type = "invalid", # Invalid cert_type
            origin = "manual",
            file_url = "media/documents/valid_doc.pdf",
            status = "pending",
            creditor = self.creditor
        )          

        with self.assertRaises(ValidationError):
            certificate.full_clean()
