<!-- Copilot / AI agent instructions for the SIGEM Flask repository -->
# Instruções rápidas para agentes de código (SIGEM Flask)

Este repositório contém um backend em Flask (Python) e um frontend em Vue 3. Abaixo estão os pontos essenciais que um agente precisa saber para ser imediatamente produtivo neste código-base.

1) Visão geral da arquitetura
- Backend: `backend/` — app Flask criado em `backend/app/__init__.py` via `create_app()`; blueprints registrados: `auth`, `scraping`, `autoprf`, `siscom`, `veiculo`, `sei`.
- Frontend: `frontend/` — Vue 3 + Vuex; scripts em `frontend/package.json`.
- Persistência: SQLite pequena usada em `backend/instance/database.db`. Migrações com Alembic/Flask-Migrate em `backend/migrations/`.
- Serviços/integrações: clientes HTTP em `backend/app/services/` (ex.: `autoprf_client.py`). Scraping usa `selenium` (ver `requirements.txt`).

2) Como rodar localmente (dev)
- Backend (PowerShell):
```powershell
cd backend
python -m pip install -r requirements.txt
# opção rápida para dev
python wsgi.py
```
O `wsgi.py` já expõe `app = create_app()` (útil para servidores WSGI) e também permite rodar o servidor de desenvolvimento.

- Banco e migrações (após instalar requirements):
```powershell
cd backend
#$env:FLASK_APP = 'backend.wsgi'    # opcional se preferir usar o CLI do Flask
python -m flask db migrate -m "mensagem"
python -m flask db upgrade
```

- Frontend:
```powershell
cd frontend
npm install
npm run serve
```

3) Padrões e convenções do projeto
- Blueprints: cada conjunto de rotas vive em `backend/app/routes/<nome>.py`. Para adicionar rota: criar blueprint e registrar em `create_app()` em `backend/app/__init__.py`.
- Serviços: código que fala com sistemas externos vai para `backend/app/services/`. Ex.: `AutoPRFClient` encapsula chamadas `requests` para `https://auto.prf.gov.br/api` (veja `BASE_URL`).
- Modelos: `backend/app/models.py` contém `User` com campos importantes: `autoprf_session`, `sei_session`, `sei_home_html`, `usuario_sei`.
- Autenticação/API: JWT é usado para sessões; tokens podem ser armazenados na coluna `autoprf_session`. Cabeçalhos Authorization são aplicados por clientes quando `self.jwt_token` estiver presente (padrão no `autoprf_client`).

4) Comportamentos específicos e mensagens esperadas
- Quando chamadas AutoPRF falham com 401/403, o backend limpa sessão e responde com mensagem `Sessão AutoPRF expirada`. O frontend também trata `Sessão não iniciada`.
- Em algumas APIs do AutoPRF, sucesso pode ser retornado como `1` ou `true` — ver como o frontend interpreta respostas ao exibir snackbars (consistência importante ao mudar backend).

5) Arquivos e configurações relevantes
- `backend/config.py` — variáveis carregadas via `.env`. Variáveis importantes: `SECRET_KEY`, `JWT_SECRET_KEY`, `CHROMEDRIVER_PATH` (selenium). Verifique esse arquivo antes de alterar o comportamento do app.
- `backend/requirements.txt` — dependências (requests, selenium, Flask, Flask-Migrate, SQLAlchemy etc.).
- `backend/wsgi.py` — ponto de entrada; expõe `app` e é usado para dev local.
- `backend/migrations/` — migrações alembic.

6) Testes e fluxo CI local
- Testes (pytest) estão no diretório `tests/`. Executar `pytest -q` a partir da raiz do repositório.
- Antes de modificar modelos, gerar migração (`flask db migrate`) e garantir que os testes relevantes passam.

7) Boas práticas específicas para agentes
- Siga os patterns existentes: crie classes clientes em `app/services/` para qualquer integração externa; mantenha tratamento de erros consistente (usar `response.raise_for_status()` quando apropriado, como em `autoprf_client.py`).
- Ao modificar modelos, lembre-se de criar uma migração e atualize `backend/instance/database.db` localmente apenas para testes — não presumir seu conteúdo.
- Para endpoints que manipulam uploads (ex.: anexar PDFs em AutoPRF), observe que o fluxo é: GET da página → POST de upload temporário → PUT para anexar (veja `anexar_documento_processo`). Reimplementar deve preservar essa sequência.

8) Pontos de atenção / riscos conhecidos
- `CHROMEDRIVER_PATH` é usado para selenium; se ausente, scraping pode falhar silenciosamente.
- JWT/segredos estão em `config.py` via `.env`; não exfiltrar chaves nem incluí-las em commits.

9) Onde editar para tarefas comuns
- Nova rota/API: `backend/app/routes/novo_recurso.py` -> registrar em `create_app()`.
- Novo cliente externo: `backend/app/services/novo_cliente.py` (simular padrão de `AutoPRFClient`).
- Alterar modelo: `backend/app/models.py` -> `flask db migrate` -> `flask db upgrade`.

Se algo estiver incompleto ou você quiser que eu adicione exemplos de arquivos/trechos (por exemplo, a forma canônica de um novo blueprint), diga quais tópicos priorizar que eu atualizo este arquivo.
