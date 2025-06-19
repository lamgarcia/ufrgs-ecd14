# ATP05  - MICROSERVIÇOS

Trabalho final para disciplina ECD14 - Arquitetura de Microserviços <br>
Aluno: Luiz Antônio Marques Garcia <br>
Professor responsável: Leandro Wives

<em></em>

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=default&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy"> <img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=default&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=default&logo=FastAPI&logoColor=white" alt="FastAPI"> <img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/GraphQL-E10098.svg?style=default&logo=GraphQL&logoColor=white" alt="GraphQL">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=default&logo=Pydantic&logoColor=white" alt="Pydantic"> <img src="https://img.shields.io/badge/YAML-CB171E.svg?style=default&logo=YAML&logoColor=white" alt="YAML">

</div>
<br>

##  Serviço de Agenda com FastAPI + GraphQL

Este projeto implementa uma **API RESTful** para gerenciar uma agenda de contatos com números de telefone, utilizando **FastAPI** e **SQLAlchemy** com banco de dados **PostgreSQL**.
Também fornece uma **API GraphQL** como camada de gateway para o serviço de agenda.


###  Funcionalidades

- Criar contatos com múltiplos números de telefone
- Listar todos os contatos
- Consultar um contato por nome
- Excluir um contato e seus telefones


###  Estrutura do Banco de Dados

#### 📄 `contatos`

| Campo     | Tipo            | Descrição                       |
|-----------|------------------|---------------------------------|
| `id`      | Integer (PK)     | Identificador único do contato |
| `nome`    | String           | Nome do contato                |
| `categoria` | Enum (`pessoal`, `familiar`, `comercial`) | Tipo de contato |
| `telefones` | Relacionamento | Lista de telefones associados  |

---

#### 📄 `telefones`

| Campo        | Tipo                            | Descrição                             |
|--------------|----------------------------------|----------------------------------------|
| `id`         | Integer (PK)                    | Identificador único do telefone       |
| `numero`     | String                          | Número de telefone                    |
| `tipo`       | Enum (`movel`, `fixo`, `comercial`) | Tipo de número                       |
| `contato_id` | Foreign Key → `contatos.id`     | Referência ao contato associado       |

---

## Estrutura do Projeto

```sh
└── atp05/
    ├── contato_service
    │   ├── Dockerfile
    │   ├── main.py
    │   └── requirements.txt
    ├── create_images.sh
    ├── graphql_api_gateway
    │   ├── Dockerfile
    │   ├── main.py
    │   ├── requirements.txt
    │   └── schema.graphql
    ├── init_containers.sh
    ├── k8s
    │   ├── contato-service-clusterip.yaml
    │   ├── contato-service-deployment.yaml
    │   ├── graphql-gateway-deployment.yaml
    │   ├── graphql-gateway-nodeport.yaml
    │   ├── postgres-deployment.yaml
    │   ├── postgres-pvc.yaml
    │   └── postgres-service.yaml
    ├── querys.txt
    ├── README.md
    └── stop_containers.sh
```
## Instalação 

Utilize um ambiente Linux com Docker ou WSL no Windows com Desktop Docker integrado.

**Clone o repositório:**

```sh
    git clone https://github.com/lamgarcia/ufrgs-ecd14.git

```
**Crie os containers:**

```sh
    sh create_images.sh
```

**Inicialize os containers:**

```sh
    sh init_containers.sh
```

## Uso dos Microserviços

**Acesse o gateway graphql:** 
No navegador abra em http://localhost:30004/graphql

## Consultas

**CRIAR CONTATOS**

<pre>
mutation {
  createContato(input: {
    nome: "Joao da Silva",
    categoria: pessoal,
    telefones: [
      { numero: "11999999999", tipo: movel },
      { numero: "1133334444", tipo: fixo }
    ]
  }) {
    message
    contato {
      id
      nome
    }
  }
}

mutation {
  createContato(input: {
    nome: "Maria da Silva",
    categoria: comercial
    telefones: [
      { numero: "41839883888", tipo: movel }
    ]
  }) {
    message
    contato {
      id
      nome
    }
  }
}
</pre>

**LISTAR TODOS OS CONTATOS**
<pre>
query {
  contatos {
    id
    nome
    categoria
    telefones {
      numero
      tipo
    }
  }
}
</pre>

**LISTAR CONTATO POR NOME**
<pre>
query {
  contatosPorNome(prefixo: "joao") {
    id
    nome
    categoria
    telefones {
      numero
      tipo
    }
  }
}
</pre>
    
**EXCLUIR CONTATO**
<pre>
mutation {
  deleteContato(id: 2) {
    message
    success
  }
}
</pre>
