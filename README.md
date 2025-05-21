# 💼 Mercatório – Backend Challenge

Projeto desenvolvido para simular a etapa de originação de precatórios, incluindo cadastro de credores, upload de documentos, consulta de certidões (manual e automática via mock) e revalidação programada com Celery.

---

## 🚀 Tecnologias

- Python 3.11
- Django 5
- Django Rest Framework
- Celery + Redis
- Bootstrap (interface simples)
- Docker + Docker Compose

---

## ⚙️ Instalação local

```bash
# Clone o repositório
git clone https://github.com/claytongit/challenge-mercatorio
cd challenge-mercatorio

# Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Linux/macOS: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser

# Rode a aplicação
python manage.py runserver
```

## 🐳 Docker
Para subir tudo com Docker + Celery + Redis:

```bash
docker-compose up --build
```

Isso sobe os serviços:
- web: Django na porta 8000
- worker: Celery worker
- beat: Celery Beat para revalidação diária
- redis: Broker para filas

## 🚀🔁 Tarefas agendadas
O sistema utiliza Celery Beat para revalidar automaticamente as certidões dos credores a cada 24h. A consulta é feita na API mock interna (/api/certidoes?cpf_cnpj=...).

## 🧪 Rodando os testes

```bash
python manage.py test
```
Testes cobrem:
- Cadastro de credores
- Upload de documentos
- Certidões (manuais e via API)
- API mock
- Serviço de revalidação
- Views e serializers

## 📬 Endpoints Principais

| Método | Rota                                     | Descrição                                      | Tipo       |
|--------|------------------------------------------|------------------------------------------------|------------|
| POST   | `/credores`                              | Cadastra credor e seu precatório               | API Rest   |
| POST   | `/credores/:id/documentos`               | Upload de documentos pessoais                  | Web (UI)   |
| POST   | `/credores/:id/certidoes`                | Upload manual de certidões                     | Web (UI)   |
| POST   | `/credores/:id/buscar-certidoes`         | Simula consulta de certidões via API mock      | API Rest   |
| GET    | `/credores/:id`                          | Consulta geral do credor                       | API Rest   |
| GET    | `/api/certidoes?cpf_cnpj=00000000000`    | Mock da API de certidões                       | API Rest   |

## 🖥 Interface web

- A aplicação possui uma interface simples com Bootstrap para:
Upload de documentos
Upload de certidões manuais

## ✅ Requisitos atendidos
- API RESTful
- Interface web simples
- Celery + agendamento com beat
- Upload e simulação de certidões
- Testes automatizados
- Dockerizado

## 📘 Documentação Swagger

O projeto inclui documentação interativa da API disponível em:
- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
