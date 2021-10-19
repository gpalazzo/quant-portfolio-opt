FROM python:3.7-slim-buster

ENV PIP_NO_CACHE_DIR=1

# install project requirements
COPY pyproject.toml .
RUN pip install poetry==1.0.10 && \
    poetry config virtualenvs.create false &&\
    poetry lock && \
    poetry install
