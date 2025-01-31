#!/bin/bash

# Отримуємо поточну директорію скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1  # Переходимо в директорію скрипта

# Перевірка та ініціалізація Git, якщо потрібно
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Initializing Git repository in $SCRIPT_DIR..."
    git init
    git branch -M main
    echo "Git repository initialized."
else
    echo "Git repository already exists in $SCRIPT_DIR."
fi

# Запуск Python-скрипта
python3 log_analyze.py "$@"
