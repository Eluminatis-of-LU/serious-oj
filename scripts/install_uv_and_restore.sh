#!/bin/bash

python3 -m pip install uv

uv venv

source .venv/bin/activate

uv pip install -r requirements.txt