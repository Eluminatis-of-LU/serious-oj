FROM node:16-buster AS stage-node
COPY . /app/src
WORKDIR /app/src

RUN yarn \
    && yarn build:production

# main
FROM ghcr.io/astral-sh/uv:python3.9-bookworm-slim
COPY --from=stage-node /app/src/vj4 /app/vj4
COPY --from=stage-node /app/src/LICENSE /app/src/README.md /app/src/requirements.txt /app/src/setup.py /app/
COPY ./scripts/restore.sh /restore.sh
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        git

RUN /restore.sh

RUN rm /restore.sh

RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV GIT_PYTHON_REFRESH=quiet
ENV VJ_LISTEN=http://0.0.0.0:8888

ADD docker-entrypoint.py /app/
ADD ./scripts/run_server_uv.sh /app/
ADD ./scripts/cli_entrypoint_uv.sh /app/

ENTRYPOINT [ "/app/cli_entrypoint_uv.sh" ]

EXPOSE 8888
CMD ["run_server_uv.sh"]
