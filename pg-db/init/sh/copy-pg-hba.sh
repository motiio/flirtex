#!/bin/bash
set -e
echo "Starting 11_pg_hba.sh"

cp /pg_hba.conf "${PGDATA}/"
