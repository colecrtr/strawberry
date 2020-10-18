FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_PATH="/app" \
    VENV_PATH="/opt/venv"

WORKDIR $APP_PATH

RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . $APP_PATH/
