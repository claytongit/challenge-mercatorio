import requests
from django.utils import timezone
from mercatorio.models import Certificate

def fetch_and_update_certificates_for(creditor):
    response = requests.get('http://localhost:8000/api/certidoes', params={'cpf_cnpj': creditor.cpf_cnpj})

    if response.status_code != 200:
        return False

    Certificate.objects.filter(creditor=creditor, origin='api').delete()
    data = response.json()    

    for cert in data['certidoes']:
        Certificate.objects.create(
            creditor=creditor,
            cert_type=cert['tipo'],
            origin='api',
            status=cert['status'],
            file_url=cert['file_url'],
            received_at=timezone.now()
        )
    return True