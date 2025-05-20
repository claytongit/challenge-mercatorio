import os
from django.core.exceptions import ValidationError

def validate_document_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError(f'Extensão não permitida: {ext}. Use: {", ".join(valid_extensions)}')

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(f'O arquivo é muito grande! Tamanho máximo permitido: 5MB.')

def validate_certificate_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf']
    if ext not in valid_extensions:
        raise ValidationError(f'Extensão não permitida: {ext}. Use: {", ".join(valid_extensions)}')