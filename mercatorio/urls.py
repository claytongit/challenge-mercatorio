from django.urls import path

from . import views

app_name = 'mercatorio'

urlpatterns = [
    path('', views.create_creditor, name='create'),
    path('/<int:pk>/documentos', views.upload_document_view, name='upload-document'),
    path('/<int:pk>/certidoes', views.upload_certificate_view, name='upload_certificate'),
    path('/<int:pk>/buscar-certidoes', views.search_certificates_view, name='search_certificates'),
]