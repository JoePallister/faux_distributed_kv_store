#!/usr/bin/env bash

set -e

KEY=$1
VALUE=$2

BASE_URL="http://127.0.0.1:8000/store"

echo "Testing posting a key-value pair"
echo "Key: $KEY"
echo "Value: $VALUE"
echo

response=$(curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"key\": \"$KEY\", \"value\": \"$VALUE\"}")

echo "Response:"
echo "$response"
echo