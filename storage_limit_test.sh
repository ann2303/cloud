docker compose --env-file ./storage_limit_proof/.env up 2> ./storage_limit_proof/test_logs > ./storage_limit_proof/test_logs &
PID=$!
sleep 120
kill $PID
