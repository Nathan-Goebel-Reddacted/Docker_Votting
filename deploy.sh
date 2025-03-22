#!/bin/bash

APP_NAME="myapp"
SECRET_NAME="db_password"
SECRET_FILE="secrets/db_password.txt"
COMPOSE_FILE="docker-compose.swarm.yml"

# Step 1: Build images
echo "Building Docker images..."
docker build -t ${APP_NAME}_vote ./vote || exit 1
docker build -t ${APP_NAME}_worker ./worker || exit 1
docker build -t ${APP_NAME}_result ./result || exit 1

# Step 2: Create secret if it doesn't exist
if docker secret ls | grep -q $SECRET_NAME; then
  echo "Secret '$SECRET_NAME' already exists, skipping creation."
else
  if [ ! -f "$SECRET_FILE" ]; then
    echo "Secret file '$SECRET_FILE' not found!"
    exit 1
  fi
  echo "Creating Docker secret '$SECRET_NAME'..."
  docker secret create $SECRET_NAME $SECRET_FILE || exit 1
fi

# Step 3: Deploy the stack
echo "Deploying stack '$APP_NAME' using $COMPOSE_FILE..."
docker stack deploy -c $COMPOSE_FILE $APP_NAME || exit 1

echo "Deployment complete!"
