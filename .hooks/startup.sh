#!/bin/bash

export PGDATA="$PROJECT_DIR/.database"
pg_ctl start -l "$PROJECT_DIR/database.log"
echo "Database has been started."

alias manage=$PROJECT_DIR/manage.py
alias daemons="compass watch $PROJECT_DIR/frontend/sass & manage runserver"
alias console="manage shell_plus"