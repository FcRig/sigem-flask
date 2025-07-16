# SIGEM Flask Backend

This repository contains a Flask backend and a Vue frontend. Database migrations are managed with Alembic.

## Database Setup

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Initialize the migration environment (only once):
   ```bash
   flask db init
   ```
   The command creates the `migrations/` directory.

3. Generate a migration after models change:
   ```bash
   flask db migrate -m "<message>"
   ```

4. Apply migrations to create or update the database:
   ```bash
   flask db upgrade
   ```

The database file will be created under `backend/instance/`.

## AutoPRF Sessions

When the backend detects that an AutoPRF request fails with status `401` or
`403`, it clears the stored session and responds with status `401` and the
message `Sessão AutoPRF expirada`. The frontend now listens for this message or
for `Sessão não iniciada` responses and displays a snackbar prompting the user
to authenticate in AutoPRF.

## SISCOM

- `POST /api/siscom/historico` – retorna o histórico do Auto de Infração.

## AutoPRF

- `POST /api/autoprf/solicitacao/cancelamento` – envia uma solicitação de
  cancelamento de Auto de Infração utilizando a sessão autenticada.
- `POST /api/autoprf/anexar/<id_processo>` – anexa um PDF ao processo antes da
  solicitação de cancelamento.
- `GET /api/autoprf/historico/<id_processo>` – obtém o histórico do processo
  de Auto de Infração utilizando a sessão autenticada.

O frontend inclui um botão **Solicitação de Cancelamento** na tela de
Veículos de Emergência que envia a requisição e exibe uma snackbar de sucesso
quando a API responde `1` ou `true`.
