#!/bin/bash
set -a
source .docker.env
set +a

docker compose -f docker-compose.test.yml up --build

