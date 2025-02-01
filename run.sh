#!/bin/bash

# Get the current directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Check and initialize Git
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Initializing Git repository in $SCRIPT_DIR..."
    git init
    git branch -M main
    echo "Git repository initialized."
else
    echo "Git repository already exists in $SCRIPT_DIR."
fi

# Running a Python script
python3 log_analyze.py "$@"
