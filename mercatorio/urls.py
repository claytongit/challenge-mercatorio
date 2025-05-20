from django.urls import path

from . import views

app_name = 'mercatorio'

urlpatterns = [
    path('', views.create_creditor, name='create'),
    path('/<int:pk>/documentos', views.upload_document_view, name='upload-document'),
]