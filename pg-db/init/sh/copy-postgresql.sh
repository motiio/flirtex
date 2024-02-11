#!/bin/bash
set -e
echo "Starting 12_postgresql.sh"

cp /postgresql.conf "${PGDATA}/"
