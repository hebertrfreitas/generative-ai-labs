#!/bin/bash

echo "Selected model: $1"
model=$1

if [ -z "$1" ]; then
    echo 'User dont selected a model, using llama3.1' 
    model="llama3.1"
fi

echo 'Removing older runs'
docker compose down -v --remove-orphans || true

echo 'running services'
docker compose up -d

echo 'Pulling the model'

docker exec -it ollama ollama pull $model