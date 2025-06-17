from fastapi import FastAPI
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.graphql import GraphQLError
from ariadne.asgi import GraphQL 
import os 
import requests

# Instância da aplicação FastAPI
app = FastAPI(
    title="GraphQL API Gateway",
    description="Gateway que agrega o serviço de Agenda de Contatos.",
)

# URL do microserviço de contatos
AGENDA_SERVICE_URL = os.getenv("AGENDA_SERVICE_URL", "http://localhost:8000")

# Carrega o esquema GraphQL
type_defs = load_schema_from_path("schema.graphql")

# Resolvers para Queries
query = QueryType()

@query.field("contatos")
async def resolve_contatos(_, info):
    try:
        response = requests.get(f"{AGENDA_SERVICE_URL}/contatos")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise GraphQLError(f"Erro ao buscar contatos: {e}")

@query.field("contato")
async def resolve_contato(_, info, id):
    try:
        response = requests.get(f"{AGENDA_SERVICE_URL}/contato/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise GraphQLError("Contato não encontrado")
        raise GraphQLError(f"Erro ao buscar contato: {e}")
    except requests.exceptions.RequestException as e:
        raise GraphQLError(f"Erro de rede: {e}")

@query.field("contatosPorNome")
async def resolve_contatos_por_nome(_, info, prefixo):
    try:
        response = requests.get(f"{AGENDA_SERVICE_URL}/contatos")
        response.raise_for_status()
        contatos = response.json()
        return [c for c in contatos if c["nome"].lower().startswith(prefixo.lower())]
    except requests.exceptions.RequestException as e:
        raise GraphQLError(f"Erro ao buscar contatos: {e}")
    
# Resolvers para Mutations
mutation = MutationType()

@mutation.field("createContato")
async def resolve_create_contato(_, info, input):
    try:
        response = requests.post(f"{AGENDA_SERVICE_URL}/contato", json=input)
        response.raise_for_status()
        return {
            "message": "Contato criado com sucesso.",
            "contato": response.json()
        }
    except requests.exceptions.RequestException as e:
        raise GraphQLError(f"Erro ao criar contato: {e}")

@mutation.field("deleteContato")
async def resolve_delete_contato(_, info, id):
    try:
        response = requests.delete(f"{AGENDA_SERVICE_URL}/contato/{id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise GraphQLError("Contato não encontrado")
        raise GraphQLError(f"Erro ao apagar contato: {e}")
    except requests.exceptions.RequestException as e:
        raise GraphQLError(f"Erro de rede ao apagar contato: {e}")
    

# Criação do schema GraphQL
schema = make_executable_schema(type_defs, query, mutation)

# Monta o endpoint do GraphQL
app.mount("/graphql", GraphQL(schema, debug=True))
