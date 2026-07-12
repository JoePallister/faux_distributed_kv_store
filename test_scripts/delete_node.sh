#!/usr/bin/env bash

set -e

NODE_NAME=$1

BASE_URL="http://127.0.0.1:8000/ring/$NODE_NAME"

echo "Testing deleting a node"
echo "Node NAME: $NODE_NAME"
echo
echo "Value: $VALUE"
echo

response=$(curl -s -X DELETE "$BASE_URL")

echo "Response:"
echo "$response"
echo