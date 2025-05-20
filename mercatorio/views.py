from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreditorSerializer
from .models import Creditor

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
