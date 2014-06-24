#!/bin/bash

pg_ctl start
echo "Database has been started."

alias manage=$PROJECT_DIR/manage.py
alias daemons="compass watch $PROJECT_DIR/frontend/sass & manage runserver"
alias console="manage shell_plus"