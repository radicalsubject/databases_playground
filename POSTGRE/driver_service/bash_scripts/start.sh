#!/bin/bash
cgrdb init -c '{"host": "postgredb_service", "password": "secret", "user": "postgres"}'
cgrdb create -c '{"host": "postgredb_service", "password": "secret", "user": "postgres"}' -n 'schema_name' -f '/db_config/config.json' || echo "key error - schema was already created"
# exec "$@" this is nessesary only when start.sh is used as entrypoint, which is not acceptable