ARG BASE_IMAGE=python:3.7-buster
FROM $BASE_IMAGE

COPY --from=python:3.7-buster / /

ENV PIP_NO_CACHE_DIR=1

## install project requirements
COPY pyproject.toml .
RUN pip install poetry && \
    poetry config virtualenvs.create false &&\
    poetry lock && \
    poetry install

WORKDIR /home/ampl
COPY . .

ENV PYTHONPATH="/home/ampl/src:${PYTHONPATH}"

ADD run.sh /tmp/run.sh
RUN chmod +x /tmp/run.sh
ENTRYPOINT ["/tmp/run.sh"]
