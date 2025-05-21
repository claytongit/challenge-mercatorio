import requests_mock
from django.test import TestCase
from django.utils import timezone
from mercatorio.models import Creditor, Certificate
from mercatorio.services.certificates import fetch_and_update_certificates_for

class FetchAndUpdateCertificatesTest(TestCase):
    def setUp(self):
        self.creditor = Creditor.objects.create(
            name='João Teste',
            cpf_cnpj='12345678900',
            email='joao@example.com',
            phone='11999999999'
        )

    def test_fetch_and_update_certificates_creates_new_records(self):
        mock_data = {
            "cpf_cnpj": "12345678900",
            "certidoes": [
                {
                    "tipo": "federal",
                    "status": "positive",
                    "file_url": "/media/certificates/federal_updated.pdf"
                },
                {
                    "tipo": "labor",
                    "status": "negative",
                    "file_url": "/media/certificates/labor_updated.pdf"
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get('http://localhost:8000/api/certidoes', json=mock_data)

            success = fetch_and_update_certificates_for(self.creditor)
            self.assertTrue(success)

            certs = Certificate.objects.filter(creditor=self.creditor, origin='api')
            self.assertEqual(certs.count(), 2)

            federal = certs.get(cert_type='federal')
            self.assertEqual(federal.status, 'positive')
            self.assertEqual(federal.file_url, '/media/certificates/federal_updated.pdf')
            self.assertAlmostEqual(federal.received_at.date(), timezone.now().date())

            labor = certs.get(cert_type='labor')
            self.assertEqual(labor.status, 'negative')
