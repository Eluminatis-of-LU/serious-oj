FROM node:14-buster AS stage-node
COPY . /app/src
WORKDIR /app/src

RUN yarn \
    && yarn build:production

# main
FROM python:3.9-slim-buster
COPY --from=stage-node /app/src/vj4 /app/vj4
COPY --from=stage-node /app/src/LICENSE /app/src/README.md /app/src/requirements.txt /app/src/setup.py /app/
COPY --from=stage-node /app/src/.git /app/.git
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        git build-essential python3-dev libffi-dev && \
    python3 -m pip install -r requirements.txt && \
    apt-get purge -y \
        build-essential && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV GIT_PYTHON_REFRESH=quiet
ENV VJ_LISTEN=http://0.0.0.0:8888

ADD docker-entrypoint.py /app/
ENTRYPOINT [ "python3", "docker-entrypoint.py" ]

EXPOSE 8888
CMD [ "vj4.server" ]