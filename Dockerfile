FROM node:14-buster AS stage-node
COPY . /app/src
WORKDIR /app/src

RUN yarn \
    && yarn build:production

# main
FROM python:3.9-buster
COPY --from=stage-node /app/src/vj4 /app/vj4
COPY --from=stage-node /app/src/LICENSE /app/src/README.md /app/src/requirements.txt /app/src/setup.py /app/
COPY --from=stage-node /app/src/.git /app/.git
COPY ./scripts/install_uv_and_restore.sh /install_uv_and_restore.sh
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        git

RUN /install_uv_and_restore.sh

RUN rm /install_uv_and_restore.sh

RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV GIT_PYTHON_REFRESH=quiet
ENV VJ_LISTEN=http://0.0.0.0:8888

ADD docker-entrypoint.py /app/
ADD ./scripts/run_server_uv.sh /app/
ADD ./scripts/cli_entrypoint_uv.sh /app/

ENTRYPOINT [ "bash", "cli_entrypoint_uv.sh" ]

EXPOSE 8888
CMD ["run_server_uv.sh"]