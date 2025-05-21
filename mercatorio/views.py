from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import random

import requests
from django.utils import timezone

from .serializers import CreditorSerializer, CreditorDetailSerializer
from .models import Creditor, PersonalDocument, Certificate
from mercatorio.forms import PersonalDocumentForm, CertificateForms

# Create your views here.
@api_view(['POST'])
def create_creditor(request):
    cpf_cnpj = request.data.get('cpf_cnpj')
    if cpf_cnpj and Creditor.objects.filter(cpf_cnpj=cpf_cnpj).exists():
        return Response({'message': 'cpf/cnpj já existe.'}, status=status.HTTP_409_CONFLICT)
    serializer = CreditorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_document_view(request, pk):
    creditor = get_object_or_404(Creditor, pk=pk)
    Personal_document = PersonalDocument.objects.filter(creditor=creditor)
    form = PersonalDocumentForm()
    if request.method == 'POST':
        form = PersonalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.creditor = creditor
            document.save()
    return render(request, 'mercatorio/index.html', {'form': form, 'creditor': creditor, 'documents': Personal_document})

def upload_certificate_view(request, pk):
    creditor = get_object_or_404(Creditor, pk=pk)
    form = CertificateForms()
    certificate = Certificate.objects.filter(creditor=creditor)
    if request.method == 'POST':
        form = CertificateForms(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.creditor = creditor
            certificate.save()
    return render(request, 'mercatorio/certificate.html', {'form': form, 'creditor': creditor, 'certificates': certificate})

@api_view(['GET'])
def mock_certificate_api(request):
    cpf_cnpj = request.GET.get('cpf_cnpj')
    if not cpf_cnpj:
        return Response({'message': 'cpf_cnpj é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

    tipos = ['federal', 'state', 'municipal', 'labor']
    status_options = ['negative', 'positive', 'invalid', 'pending']

    certidoes = []
    for tipo in tipos:
        certidoes.append({
            'tipo': tipo,
            'status': random.choice(status_options),
            'file_url': f"/media/certificates/{tipo}_fake_certidao.pdf"
        })
    
    return Response({
        'cpf_cnpj': cpf_cnpj,
        'certidoes': certidoes
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def search_certificates_view(request, pk):
    creditor = get_object_or_404(Creditor, pk=pk)
    cpf_cnpj = creditor.cpf_cnpj

    response = requests.get('http://localhost:8000/api/certidoes', params={'cpf_cnpj': cpf_cnpj})

    if response.status_code != 200:
        return Response({'message': 'rro ao consultar certidões'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = response.json()

    for cert in data['certidoes']:
        Certificate.objects.create(
            creditor=creditor,
            cert_type=cert['tipo'],
            status=cert['status'],
            origin='api',
            file_url=cert['file_url'],
            received_at=timezone.now()
        )

    return Response({'message': 'Certidões geradas com sucesso'}, status = status.HTTP_200_OK)

@api_view(['GET'])
def creditor_detail_view(request, pk):
    creditor = get_object_or_404(Creditor, pk=pk)
    serializer = CreditorDetailSerializer(creditor)
    return Response(serializer.data)