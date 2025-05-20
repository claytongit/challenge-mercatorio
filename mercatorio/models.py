from django.db import models
from django.utils import timezone

# Create your models here.
class Creditor(models.Model):
    name = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"

class Precatorio(models.Model):
    precatorio_number = models.CharField(max_length=100, unique=True)
    nominal_value = models.DecimalField(max_digits=15, decimal_places=2)
    forum = models.CharField(max_length=255)
    publication_date = models.DateField()

    creditor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='precatorios')

    def __str__(self):
        return f"Precatório {self.precatorio_number} - {self.creditor.name}"

class PersonalDocument(models.Model):
    class DocumentType(models.TextChoices):
        RG = 'RG', 'RG'
        CPF = 'CPF', 'CPF'
        CNH = 'CNH', 'CNH'
        BIRTH_CERTIFICATE = 'birth_certificate', 'Certidão de Nascimento'
        PROOF_OF_ADDRESS = 'proof_of_address', 'Comprovante de endereço'

    doc_type = models.CharField(max_length=50, choices=DocumentType.choices)
    file_url = models.URLField()
    submitted_at = models.DateTimeField(default=timezone.now)

    creditor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='documents')
    
    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.creditor.name}"