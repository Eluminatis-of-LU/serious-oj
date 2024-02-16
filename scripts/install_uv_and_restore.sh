#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.cargo/env

uv venv

source .venv/bin/activate

uv pip install -r requirements.txt