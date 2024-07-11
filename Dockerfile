FROM python:3.10.11


ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1\
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'\
    POETRY_VERSION=1.8.3

ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p /usr/src/app/

RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /usr/src/app/

WORKDIR /usr/src/app/

RUN  poetry config virtualenvs.create false && poetry install

CMD [ "python", "main.py"]
