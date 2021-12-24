ARG BASE_IMAGE=python:3.7-buster
FROM $BASE_IMAGE

COPY --from=python:3.7-buster / /

ENV PIP_NO_CACHE_DIR=1

# install project requirements
COPY pyproject.toml .
RUN pip install poetry && \
    poetry config virtualenvs.create false &&\
    poetry lock && \
    poetry install

ARG ROOT_DIR=/app
# set work dir as /app
WORKDIR $ROOT_DIR
ENV PROJECT_ROOT_PATH=$ROOT_DIR

# copy the entire project
COPY . .

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# serve the api when container starts
ENTRYPOINT ["python", "./src/app.py"]
