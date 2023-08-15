FROM python:3.11-alpine

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_ROOT_USER_ACTION=ignore

COPY pyproject.toml poetry.lock ./app/ ./

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir poetry \
 && poetry install --only main

EXPOSE 5000

CMD ["poetry", "run", "flask", "--app", "wsgi", "run", "--host", "0.0.0.0", "--debug"]
