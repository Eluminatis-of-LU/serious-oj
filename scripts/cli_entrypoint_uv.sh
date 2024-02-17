#!/bin/bash

source .venv/bin/activate

./docker-entrypoint.py "${@:1}"