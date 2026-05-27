# Yoda Speak

Small Django demo app that translates plain English into a Yoda-style response.

## Stack

- Django 5
- Django Ninja
- OpenAI API
- Bootstrap 4
- Docker Compose for optional multi-container demos

## Project layout

- `config/`: Django project configuration
- `yodaspeak/`: app views, API, tests, templates, and static assets
- `config/yodaspeak_prompt.txt`: system prompt sent to OpenAI
- `config/translate_samples.json`: optional built-in sample translations

## Running locally

1. Copy `.env.example` to `.env`.
2. Set `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, and optionally `OPENAI_API_KEY`.
3. Install the dependencies:
   - `make install` (recommended), or
   - `python3 -m venv .venv && .venv/bin/pip install -r requirements/local.txt`
4. Run migrations: `.venv/bin/python manage.py migrate`
5. Start the server: `.venv/bin/python manage.py runserver`

## Running with Docker

```sh
docker compose up --build
```

The GitHub Actions workflow at `.github/workflows/publish-ghcr.yml` publishes that image to GHCR on pushes to `main` and on version tags like `v1.0.0`.

The app is served on port `8000` by default. The default `.env` uses SQLite and does not require Redis. To exercise the multi-container path, switch `DATABASE_ENGINE=POSTGRES` and `CACHE_ENABLED=true`.

## Environment variables

- `DEBUG`: enables Django debug mode
- `ALLOWED_HOSTS`: comma-separated list of allowed hosts
- `DATABASE_ENGINE`: `SQLITE` or `POSTGRES`
- `CACHE_ENABLED`: enables Redis-backed cache and Redis health checks
- `OPENAI_API_KEY`: API key for live translations
- `OPENAI_MODEL`: model name used for translations
- `TRANSLATE_SAMPLES_ENABLED`: when true, uses `translate_samples.json`

## Tests

```sh
python manage.py test
```

## Notes

- The API endpoint is `POST /api/translate`.
- If sample translations are enabled and a matching sample exists, the app returns that sample instead of calling OpenAI.
- Redis is conditional and only used when `CACHE_ENABLED=true` (see `config/settings.py`).
- With `CACHE_ENABLED=false`, the app runs without Redis.
- The provided `docker-compose.yaml` still starts Redis and Postgres services for consistency with multi-service demos.
- This project is intentionally lightweight and is meant to stay a simple demo.
- SQLite is the simplest local path. Postgres and Redis are still available for container and multi-service demos.
