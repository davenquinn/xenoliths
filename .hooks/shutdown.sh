#!/bin/bash

export PGDATA="$PROJECT_DIR/.database"
pg_ctl stop
echo "Database has been shut down."