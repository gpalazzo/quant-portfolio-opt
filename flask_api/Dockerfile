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

# set work dir as /app
WORKDIR /app

# copy the entire project
COPY . .

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# expose container port 5000
#EXPOSE 5000

# serve the api when container starts
ENTRYPOINT ["python", "./src/app.py"]
