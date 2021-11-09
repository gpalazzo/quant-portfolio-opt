FROM apache/airflow:2.1.2-python3.7

ENV PIP_NO_CACHE_DIR=1

# install project requirements
COPY pyproject.toml .
RUN pip install poetry && \
    poetry config virtualenvs.create false &&\
    poetry lock && \
    poetry install

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
