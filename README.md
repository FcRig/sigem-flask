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

When the backend detects that an AutoPRF request failed with status `401` or
`403`, it clears the stored session and responds with status `401` and the
message `Sessão AutoPRF expirada`. The frontend intercepts this response,
logs the user out and shows a snackbar saying `Sessão expirada` before
redirecting to the home page.

## SISCOM

- `POST /api/siscom/historico` – retorna o histórico do Auto de Infração.
