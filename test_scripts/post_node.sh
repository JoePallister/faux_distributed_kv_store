#!/usr/bin/env bash

set -e

NODE_NAME=$1


BASE_URL="http://127.0.0.1:8000/ring/$NODE_NAME"

echo "Testing adding a node"
echo "NODE_NAME: $NODE_NAME"
echo

response=$(curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
)

echo "Response:"
echo "$response"
echo