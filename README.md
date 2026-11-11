# CRUD de Funcionários

Aplicação web para cadastrar, listar, editar e excluir funcionários, com persistência em PostgreSQL e execução com Docker Compose.

## Tecnologias
- Python 3.12
- Flask
- Flask-SQLAlchemy
- PostgreSQL 16
- Docker e Docker Compose

## Como executar
1. Instale o Docker Desktop (ou Docker Engine com o plugin Compose).
2. Na pasta do projeto, execute:
   ```bash
   docker compose up --build
   ```
3. Acesse http://localhost:5000.

O PostgreSQL fica disponível internamente para a aplicação no serviço `db`. Para encerrar, use `docker compose down`. Para apagar também os dados persistidos, use `docker compose down -v`.

## Funcionalidades
- Cadastrar funcionário com nome e CPF.
- Listar funcionários.
- Editar nome e CPF.
- Excluir funcionário.
- Validar CPF e impedir duplicidade.

## Estrutura
```text
crudfuncionarios/
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env.example
├── .gitignore
└── templates/
    ├── base.html
    ├── index.html
    └── editar.html
```

## Configuração
O Compose usa valores de desenvolvimento definidos em `compose.yaml`. Para personalizar, copie `.env.example` para `.env` e ajuste as variáveis. Não use credenciais de desenvolvimento em produção.

Projeto acadêmico desenvolvido com apoio de IA.