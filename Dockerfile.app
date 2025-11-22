FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /web

COPY pyproject.toml poetry.lock README.md ./

RUN pip install --upgrade pip wheel poetry
RUN poetry config virtualenvs.create false --local

RUN poetry install

COPY ./app ./app

WORKDIR ./app

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
