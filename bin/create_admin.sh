#!/bin/bash
set -a
source .docker.env
set +a

# Check if both email and password are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <email> <password>"
    exit 1
fi

EMAIL=$1
PASSWORD=$2

# Run the create_admin script inside the web container
docker compose exec web python scripts/create_admin.py --email "$EMAIL" --password "$PASSWORD"
