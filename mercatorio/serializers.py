from rest_framework import serializers
from .models import Creditor, Precatorio


class PrecatórioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precatorio
        fields = ['precatorio_number', 'nominal_value', 'forum', 'publication_date']


class CreditorSerializer(serializers.ModelSerializer):
    precatorio = PrecatórioSerializer(write_only=True)

    class Meta:
        model = Creditor
        fields = ['id', 'name', 'cpf_cnpj', 'email', 'phone', 'precatorio']

    def create(self, validated_data):
        precatorio_data = validated_data.pop('precatorio')
        creditor = Creditor.objects.create(**validated_data)
        Precatorio.objects.create(creditor=creditor, **precatorio_data)
        return creditor
