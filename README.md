# Health API

API RESTful para gerenciamento de consultas médicas e profissionais da saúde, construída com Django, Django REST Framework, PostgreSQL, Docker e Poetry.

## Visão geral

O projeto atende aos requisitos centrais do desafio:

- CRUD completo de profissionais da saúde
- CRUD completo de consultas
- Busca de consultas pelo ID do profissional
- Autenticação com JWT
- Validação e sanitização de dados com `bleach`
- CORS configurado via ambiente
- Logs de acesso e erro via middleware e logging do Django
- Documentação interativa com Swagger e Redoc

## Decisões técnicas

- JWT foi escolhido para autenticação básica porque reduz superfície de sessão e funciona bem em integrações externas.
- A persistência usa ORM do Django, o que elimina montagem manual de SQL e reduz risco de SQL Injection.
- `bleach` é usado na sanitização de campos textuais para reduzir risco de payloads maliciosos em inputs simples.
- `drf-spectacular` foi adotado para documentação OpenAPI pronta para uso com Swagger e Redoc.
- O CORS é controlado por variável de ambiente para não abrir origens em produção por engano.
- O logging é centralizado no Django e complementado por middleware para registrar chamadas HTTP com tempo e status.

## Setup local com Poetry

1. Instale as dependências.

   ```bash
   poetry install
   ```

2. Ajuste as variáveis de ambiente.

   Copie `.env.example` para `.env` e altere os valores necessários.

3. Rode as migrações.

   ```bash
   poetry run python manage.py migrate
   ```

4. Crie um usuário administrador se quiser acessar o admin.

   ```bash
   poetry run python manage.py createsuperuser
   ```

5. Suba a aplicação.

   ```bash
   poetry run python manage.py runserver
   ```

## Setup com Docker

1. Copie `.env.example` para `.env`.
2. Suba os serviços.

   ```bash
   docker compose up --build
   ```

3. A API ficará disponível em `http://localhost:8000`.

## Testes automatizados

Os testes usam `APITestCase`.

```bash
poetry run python manage.py test
```

Cobertura incluída:

- CRUD de profissionais
- CRUD de consultas
- Busca de consultas por ID do profissional
- Cenários inválidos e campos ausentes

## CI/CD

O workflow em [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) está organizado em quatro etapas:

1. `lint` com `flake8`
2. `test` com banco PostgreSQL em serviço de CI
3. `build` da imagem Docker
4. `deploy` para staging e produção em AWS

### Fluxo de deploy

- `develop` aciona deploy em staging
- `main` aciona deploy em produção
- A imagem é versionada pelo hash do commit
- O deploy usa ECS como destino de referência


## Observações finais

- Os retornos da API são JSON.
- A autenticação é exigida para os endpoints de negócio.
- A documentação OpenAPI fica acessível sem autenticação para facilitar consumo e testes.