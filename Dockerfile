# Étape 1: Utilisation de l'image de base Python
FROM python:3.12-slim

# Met en cache la sortie du buffer Python
ENV PYTHONUNBUFFERED=1

# Mise à jour des sources pour utiliser HTTPS
RUN find /etc/apt/ -name '*.sources' -exec sed -i 's|^\(URIs: \)http://|\1https://|' {} +

# Installation des dépendances du système nécessaires pour 'asyncpg' et 'psycopg2'
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    python3-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation de psycopg2-binary
RUN pip install psycopg2-binary

# Définition du répertoire de travail
WORKDIR /app/

# Installation de uv (copie depuis l'image fournie)
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Ajout du chemin d'environnement virtuel au PATH
ENV PATH="/app/.venv/bin:$PATH"

# Compilation du bytecode (bonne pratique uv)
ENV UV_COMPILE_BYTECODE=1

# Mode de lien du cache uv (bonne pratique uv)
ENV UV_LINK_MODE=copy

# Timeout pour les requêtes HTTP (bonne pratique uv)
ENV UV_HTTP_TIMEOUT=3000

# Copie des fichiers de configuration
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

# Installation des dépendances du projet (via le lock file)
# CORRECTION: Suppression de '--frozen' car le lock file est invalide/simulé au début.
# uv le générera/validera à la place.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync

# Chemin Python pour les importations de modules
ENV PYTHONPATH=/app

# Copie du code source et des scripts
COPY ./scripts /app/scripts
COPY ./src /app/src
COPY ./fixture_data /app/fixture_data

# Synchronisation finale après copie du code 
# Cette étape est moins nécessaire maintenant que la première étape n'est pas --frozen, 
# mais je la conserve par prudence pour le dev-dependencies (si le code src affectait les dev deps).
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Commande par défaut pour démarrer l'API
CMD ["fastapi", "run", "--host", "0.0.0.0", "--workers", "4", "src/main.py", "--port", "${API_PORT:-8000}"]