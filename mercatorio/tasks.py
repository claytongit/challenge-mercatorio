from celery import shared_task
from datetime import datetime

from mercatorio.models import Creditor
from mercatorio.services.certificates import fetch_and_update_certificates_for

@shared_task
def revalidate_certificates():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for creditor in Creditor.objects.all():
        success = fetch_and_update_certificates_for(creditor)
        if success:
            print(f"✔️ Certidões atualizadas para: {creditor.name} ... [{now}]")
        else:
            print(f"❌ Falha ao buscar certidões para: {creditor.name} ... [{now}]")