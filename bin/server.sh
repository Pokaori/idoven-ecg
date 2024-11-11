#!/bin/bash
set -a
source .docker.env
set +a

docker compose up --build
