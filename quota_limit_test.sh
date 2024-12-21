docker compose --env-file ./quota_limit_proof/.env up 2> ./quota_limit_proof/test_logs > ./quota_limit_proof/test_logs &
PID=$!
sleep 240
kill $PID