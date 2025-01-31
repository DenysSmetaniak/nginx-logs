# Nginx Log Analyzer

## Опис
Цей скрипт аналізує логи Nginx, конвертує їх у CSV і дозволяє виконувати фільтрування та сортування.

## Використання
### Запуск локально
1. Встановіть Python 3.10.
2. Запустіть:
   ```bash
   python analyze_logs.py --log-file logs/nginx.log --output-file output/logs.csv
