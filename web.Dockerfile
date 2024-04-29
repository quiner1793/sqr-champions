# Creating a python base with shared environment variables
FROM python:3.11-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ARG project_root=/web

# Install and upgrade pip and poetry
RUN pip install --upgrade pip poetry

# Copy Python requirements here to cache them and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY frontend/pyproject.toml ./
RUN poetry install --only main && \
    mkdir ${project_root}

WORKDIR ${project_root}
# Copy and give permissions for docker entrypoint
COPY ./docker-entrypoint.sh ./run_web.sh /
RUN chmod +x /docker-entrypoint.sh /run_web.sh

# Create user with the name poetry and give permissions to project_root dir
RUN groupadd -g 1500 poetry && \
    useradd -m -u 1500 -g poetry poetry

# Copy rest of application
COPY ./frontend ${project_root}/frontend

# Run as poetry user
USER poetry

EXPOSE 8501

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "/run_web.sh" ]
