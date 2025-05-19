from django.db import models

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