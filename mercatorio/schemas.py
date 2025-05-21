from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from .serializers import CreditorSerializer, CreditorDetailSerializer

create_creditor_schema = extend_schema(
    request=CreditorSerializer,
    responses={201: CreditorSerializer, 400: dict, 409: dict},
)

mock_cert_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name='cpf_cnpj',
            type=str,
            location=OpenApiParameter.QUERY,
            description='CPF ou CNPJ obrigatório para consulta',
            required=True,
        )
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'cpf_cnpj': {'type': 'string'},
                'certidoes': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'tipo': {'type': 'string'},
                            'status': {'type': 'string'},
                            'file_url': {'type': 'string'},
                        }
                    }
                }
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'}
            }
        }
    }
)

creditor_detail_schema = extend_schema(
    responses={200: CreditorDetailSerializer}
)

search_certificates_schema = extend_schema(
    responses={
        200: OpenApiResponse(description='Certidões geradas com sucesso'),
        500: OpenApiResponse(description='Erro ao consultar certidões'),
    }
)