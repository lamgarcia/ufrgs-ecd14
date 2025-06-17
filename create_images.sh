#!/bin/bash
# Para o Serviço de Produtos
docker build -t contato-service:latest ./contato_service

# Para o GraphQL API Gateway
docker build -t graphql-api-gateway:latest ./graphql_api_gateway
