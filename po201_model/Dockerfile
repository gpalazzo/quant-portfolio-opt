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

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -d /home/kedro -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro

# copy the whole project except what is in .dockerignore
WORKDIR /home/kedro
COPY . .
RUN chown -R kedro:${KEDRO_GID} /home/kedro
USER kedro
RUN chmod -R a+w /home/kedro

EXPOSE 8888

# start jupyter to keep container running in dev cycle
CMD ["kedro", "jupyter", "lab", "--no-browser"]