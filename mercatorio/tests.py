from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import Creditor, Precatorio, PersonalDocument

# Create your tests here.
class ModelsTest(TestCase):
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
        self.personal_document = PersonalDocument.objects.create(
            doc_type = "RG",
            file_url = "http://example.com/rg.pdf",
            creditor = self.creditor
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

    def test_personal_document_creation(self):
        self.assertEqual(self.personal_document.doc_type, "RG")
        self.assertEqual(self.personal_document.file_url, "http://example.com/rg.pdf")
        self.assertEqual(str(self.personal_document), "RG - Test Creditor")
    
    def test_personal_document_creation_invalid_creditor_null(self):
        with self.assertRaises(IntegrityError):
            PersonalDocument.objects.create(
                doc_type = "RG",
                file_url = "http://example.com/rg.pdf",
                creditor = None # Creditor Null
            )

    def test_personal_document_creation_invalid_doc_type(self):
        personal_document = PersonalDocument.objects.create(
            doc_type = "PIS", # Invalid doc_type
            file_url = "http://example.com/rg.pdf",
            creditor = self.creditor
        )          

        with self.assertRaises(ValidationError):
            personal_document.full_clean()
