from django.urls import path

from . import views

app_name = 'mercatorio'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('credores', views.create_creditor, name='create'),
    path('credores/<int:pk>/documentos', views.upload_document_view, name='upload-document'),
    path('credores/<int:pk>/certidoes', views.upload_certificate_view, name='upload_certificate'),
    path('credores/<int:pk>/buscar-certidoes', views.search_certificates_view, name='search_certificates'),
    path('credores/<int:pk>', views.creditor_detail_view, name='creditor_detail'),
]