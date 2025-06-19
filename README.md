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
