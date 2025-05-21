from rest_framework import serializers
from .models import Creditor, Precatorio, PersonalDocument, Certificate


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

class PersonalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDocument
        fields = ['doc_type', 'file_url', 'submitted_at']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['cert_type', 'status', 'origin', 'file_url', 'received_at']

class CreditorDetailSerializer(serializers.ModelSerializer):
    precatorio = serializers.SerializerMethodField()
    documents = PersonalDocumentSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)

    class Meta:
        model = Creditor
        fields = ['id', 'name', 'cpf_cnpj', 'email', 'phone', 'precatorio', 'documents', 'certificates']

    def get_precatorio(self, obj):
        precatorio = obj.precatorios.first()
        if precatorio:
            return PrecatórioSerializer(precatorio).data
        return None