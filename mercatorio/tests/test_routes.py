import json
from django.test import TestCase

class RoutesTest(TestCase):
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