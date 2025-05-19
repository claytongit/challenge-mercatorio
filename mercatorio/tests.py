from django.test import TestCase
from django.db import IntegrityError

from .models import Creditor

# Create your tests here.
class ModelsTest(TestCase):
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