#!/bin/bash

# curl -LsSf https://astral.sh/uv/install.sh | sh

python3 -m pip install uv

uv venv

source .venv/bin/activate

uv pip install -r requirements.txt