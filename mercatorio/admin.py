from django.contrib import admin

from .models import Creditor, Precatorio

# Register your models here.
@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    ordering = ('-id',)

class PrecatorioAdmin(admin.ModelAdmin):
    list_display = ('id','precatorio_number','creditor')
    ordering = ('-id',)

admin.site.register(Precatorio, PrecatorioAdmin)