#!/usr/bin/env bash

set -e

NODE_ID=$1

BASE_URL="http://127.0.0.1:8000/store/$NODE_ID"

echo "Testing deleting a node"
echo "Node ID: $NODE_ID"
echo
echo "Value: $VALUE"
echo

response=$(curl -s -X DELETE "$BASE_URL")

echo "Response:"
echo "$response"
echo