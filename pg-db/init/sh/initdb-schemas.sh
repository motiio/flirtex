#!/bin/bash

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"
echo "Starting 13_initdb-schemas.sh"


# Create the 'template_postgis' template db
"${psql[@]}" <<- 'EOSQL'
CREATE schema if not exists core;
EOSQL


