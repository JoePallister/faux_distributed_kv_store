#!/usr/bin/env bash

set -e

BASE_URL="http://127.0.0.1:8000/store"

echo "Testing getting all key-value pairs"
echo

response=$(curl -s -X GET "$BASE_URL")

echo "Response:"
echo "$response"
echo