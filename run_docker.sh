#!/bin/bash
# run_docker.sh — Quick launcher for LangGraph Research in Docker (WSL 2)

echo "🐳 Starting Docker daemon..."
dockerd --iptables=false --dns 8.8.8.8 > /dev/null 2>&1 &
sleep 3

echo "🔍 Checking Docker..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker failed to start."
    exit 1
fi

echo "🐳 Docker is running!"
echo "🚀 Launching LangGraph Multi-Agent Research..."
docker run -it --rm --network=host --env-file .env langgraph-research:latest