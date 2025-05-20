from django.contrib import admin

from .models import Creditor, Precatorio, PersonalDocument


# Register your models here.
@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    ordering = ('-id',)

@admin.register(Precatorio)
class PrecatorioAdmin(admin.ModelAdmin):
    list_display = ('id','precatorio_number','creditor')
    ordering = ('-id',)

@admin.register(PersonalDocument)
class PersonalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id','doc_type','creditor', 'file_url',)
    ordering = ('-id',)
